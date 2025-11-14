from collections.abc import AsyncGenerator
from typing import Any

from asgiref.sync import sync_to_async
from datastar_py.consts import ElementPatchMode
from datastar_py.django import DatastarResponse
from datastar_py.django import ServerSentEventGenerator
from datastar_py.django import datastar_response
from datastar_py.django import read_signals
from django.conf import settings
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import aget_object_or_404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import translation
from django.views import View
from django.views.decorators.http import require_http_methods

from recipe_viewer.apps.recipes.forms import IngredientFormSet
from recipe_viewer.apps.recipes.forms import RecipeForm
from recipe_viewer.apps.recipes.models import Ingredient
from recipe_viewer.apps.recipes.models import Recipe


def _build_recipe_forms(request: HttpRequest, recipe: Recipe | None = None) -> tuple[RecipeForm, IngredientFormSet]:
    data = request.POST if request.method == "POST" else None
    files = request.FILES if request.method == "POST" else None
    form = RecipeForm(data=data, files=files, instance=recipe)
    formset_instance = recipe if recipe is not None else Recipe()
    ingredient_formset = IngredientFormSet(data=data, files=files, instance=formset_instance)
    return form, ingredient_formset


def _render_recipe_form(
    request: HttpRequest,
    form: RecipeForm,
    ingredient_formset: IngredientFormSet,
    recipe: Recipe | None = None,
    status: int = 200,
) -> HttpResponse:
    context = {
        "recipe": recipe if recipe is not None else Recipe(),
        "form": form,
        "ingredient_formset": ingredient_formset,
    }
    return render(request, "recipes/recipe_creation_form.html", context, status=status)


@require_http_methods(["GET"])
async def recipe_list(request: HttpRequest) -> HttpResponse:
    """Display list of all recipes"""
    recipes: list[Recipe] = [recipe async for recipe in Recipe.objects.all().order_by("-created_at")]
    return render(request, "recipes/recipe_list.html", {"recipes": recipes})


class RecipeCreateView(View):
    """Shared logic for creating and editing recipes with their ingredients."""

    async def get(self, request: HttpRequest) -> HttpResponse:
        form, ingredient_formset = _build_recipe_forms(request)
        return _render_recipe_form(request, form=form, ingredient_formset=ingredient_formset)

    async def post(self, request: HttpRequest) -> HttpResponse:
        form, ingredient_formset = _build_recipe_forms(request)

        if form.is_valid() and ingredient_formset.is_valid():
            saved_recipe = await sync_to_async(form.save)()
            ingredient_formset.instance = saved_recipe
            await sync_to_async(ingredient_formset.save)()
            return redirect("recipe_detail", recipe_id=saved_recipe.pk)

        return _render_recipe_form(request, form=form, ingredient_formset=ingredient_formset, status=400)


class RecipeDetailView(View):
    async def get(self, request: HttpRequest, recipe_id: int) -> HttpResponse:
        """Display recipe details with portions input (default=1)"""
        recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
        ingredients: list[Ingredient] = [ingredient async for ingredient in recipe.ingredients.all()]

        user = await request.auser()

        can_change = await user.ahas_perm("recipes.change_recipe")
        can_delete = await user.ahas_perm("recipes.delete_recipe")
        return render(
            request,
            "recipes/recipe_detail.html",
            {"recipe": recipe, "ingredients": ingredients, "can_change": can_change, "can_delete": can_delete},
        )

    async def delete(self, request: HttpRequest, recipe_id: int) -> HttpResponse:
        """Delete recipe"""
        # Check permission
        user = await request.auser()
        if not await user.ahas_perm("recipes.delete_recipe"):
            return HttpResponse("Permission denied", status=403)

        recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
        await recipe.adelete()
        return redirect("recipe_list")


class RecipeChangeView(View):
    async def get(self, request: HttpRequest, recipe_id: int) -> HttpResponse:
        recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
        form, ingredient_formset = _build_recipe_forms(request, recipe)
        return _render_recipe_form(request, recipe, form, ingredient_formset)

    async def post(self, request: HttpRequest, recipe_id: int) -> HttpResponse:
        recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
        form, ingredient_formset = _build_recipe_forms(request, recipe)

        if form.is_valid() and ingredient_formset.is_valid():
            await form.asave()
            await sync_to_async(ingredient_formset.save)()
            return redirect("recipe_detail", recipe_id=recipe.id)

        return _render_recipe_form(request, recipe, form, ingredient_formset, status=400)


@datastar_response
async def recipe_ingredients(request: HttpRequest, recipe_id: int) -> AsyncGenerator[Any, None]:
    """Return updated ingredients HTML based on portions parameter"""
    recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
    ingredients: list[Ingredient] = [ingredient async for ingredient in recipe.ingredients.all()]
    signals: dict[str, Any] | None = read_signals(request)

    if signals is None:
        signals = {}

    # Calculate quantities based on portions
    calculated_ingredients: list[dict[str, Any]] = [
        {"name": ing.name, "quantity": ing.quantity * signals["portions"], "unit": ing.unit} for ing in ingredients
    ]

    rendered_html: str = render_to_string("recipes/_ingredients.html", {"ingredients": calculated_ingredients})

    yield ServerSentEventGenerator.patch_elements(rendered_html)


def _extract_formset_prefix(data: dict[str, Any]) -> str | None:
    for key in data:
        if key.endswith("-TOTAL_FORMS"):
            return key.rsplit("-", 1)[0]
    return None


@require_http_methods(["POST"])
def add_ingredient_form(request: HttpRequest) -> HttpResponse:
    """Morph the entire ingredient section after add/remove actions."""
    data = request.POST.copy()
    action = data.get("form_action")
    if not action:
        return HttpResponseBadRequest("Missing form action.")

    recipe: Recipe | None = None
    recipe_id = data.get("recipe_id")
    if recipe_id:
        try:
            recipe_pk = int(recipe_id)
        except (TypeError, ValueError):
            return HttpResponseBadRequest("Invalid recipe id.")
        recipe = get_object_or_404(Recipe, id=recipe_pk)

    prefix = _extract_formset_prefix(data)
    if prefix is None:
        return HttpResponseBadRequest("Missing management form data.")

    total_key = f"{prefix}-TOTAL_FORMS"
    try:
        current_total = int(data.get(total_key, 0))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid management form counts.")

    if action == "add_ingredient":
        data[total_key] = str(current_total + 1)
    elif action.startswith("remove:"):
        form_prefix = action.split(":", 1)[1]
        delete_key = f"{form_prefix}-DELETE"
        data[delete_key] = "on"
    else:
        return HttpResponseBadRequest("Unknown form action.")

    formset_instance = recipe if recipe is not None else Recipe()
    ingredient_formset = IngredientFormSet(
        data=data,
        files=request.FILES,
        instance=formset_instance,
        prefix=prefix,
    )

    rendered_section = render_to_string(
        "recipes/_ingredient_section.html",
        {
            "ingredient_formset": ingredient_formset,
            "recipe": formset_instance,
        },
        request=request,
    )

    return DatastarResponse(
        ServerSentEventGenerator.patch_elements(
            rendered_section,
            selector="#ingredients-section",
            mode=ElementPatchMode.REPLACE,
        )
    )


@require_http_methods(["POST"])
async def set_language(request: HttpRequest) -> HttpResponse:
    """
    Set user's preferred language.
    This is a synchronous view as it works with cookies and sessions.
    """
    language_code = request.POST.get("language", request.GET.get("language", settings.LANGUAGE_CODE))

    # Validate language code
    if language_code not in [lang[0] for lang in settings.LANGUAGES]:
        language_code = settings.LANGUAGE_CODE

    # Activate the language for the current thread
    translation.activate(language_code)

    # Get the redirect URL (either from POST/GET or fallback to referer or home)
    next_url = request.POST.get("next", request.GET.get("next", request.META.get("HTTP_REFERER", "/")))

    response = redirect(next_url)

    # Set the language cookie so it persists across requests
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        language_code,
        max_age=settings.LANGUAGE_COOKIE_AGE if hasattr(settings, "LANGUAGE_COOKIE_AGE") else 31536000,  # 1 year
        path=settings.LANGUAGE_COOKIE_PATH if hasattr(settings, "LANGUAGE_COOKIE_PATH") else "/",
        domain=settings.LANGUAGE_COOKIE_DOMAIN if hasattr(settings, "LANGUAGE_COOKIE_DOMAIN") else None,
        secure=settings.LANGUAGE_COOKIE_SECURE if hasattr(settings, "LANGUAGE_COOKIE_SECURE") else False,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY if hasattr(settings, "LANGUAGE_COOKIE_HTTPONLY") else False,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE if hasattr(settings, "LANGUAGE_COOKIE_SAMESITE") else None,
    )

    return response
