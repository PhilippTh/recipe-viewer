import math
from collections.abc import AsyncGenerator
from typing import Any

from asgiref.sync import sync_to_async
from datastar_py.consts import ElementPatchMode
from datastar_py.django import DatastarResponse
from datastar_py.django import ServerSentEventGenerator
from datastar_py.django import datastar_response
from datastar_py.django import read_signals
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import aget_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
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


async def _user_has_any_permission(request: HttpRequest, *permissions: str) -> bool:
    user = await request.auser()
    is_authenticated = bool(getattr(user, "is_authenticated", False))
    if not is_authenticated:
        return False
    for permission in permissions:
        if await user.ahas_perm(permission):
            return True
    return False


def _normalize_portions(signals: dict[str, Any] | None) -> float:
    """Ensure the portions multiplier is a positive, finite float."""
    if not signals:
        return 1.0
    raw_value = signals.get("portions", 1.0)
    try:
        portions = float(raw_value)
    except (TypeError, ValueError):
        return 1.0
    if not math.isfinite(portions):
        return 1.0
    return max(portions, 0.5)


async def _render_recipe_form(
    request: HttpRequest,
    form: RecipeForm,
    ingredient_formset: IngredientFormSet,
    recipe: Recipe | None = None,
    status: int = 200,
    action_url: str | None = None,
    cancel_url: str | None = None,
) -> HttpResponse:
    context = {
        "recipe": recipe if recipe is not None else Recipe(),
        "form": form,
        "ingredient_formset": ingredient_formset,
        "form_action": action_url or request.path,
        "cancel_url": cancel_url or reverse("recipe_list"),
    }
    return await sync_to_async(render)(
        request=request,
        template_name="recipes/recipe_form.html",
        context=context,
        status=status,
    )


@require_http_methods(["GET"])
async def recipe_list(request: HttpRequest) -> HttpResponse:
    """Display list of all recipes"""
    recipes: list[Recipe] = [recipe async for recipe in Recipe.objects.all().order_by("-created_at")]
    return await sync_to_async(render)(
        request=request,
        template_name="recipes/recipe_list.html",
        context={"recipes": recipes},
    )


class RecipeCreateView(View):
    """Shared logic for creating and editing recipes with their ingredients."""

    async def get(self, request: HttpRequest) -> HttpResponse:
        if not await _user_has_any_permission(request, "recipes.add_recipe"):
            return HttpResponse(status=403)
        form, ingredient_formset = _build_recipe_forms(request)
        return await _render_recipe_form(
            request,
            form=form,
            ingredient_formset=ingredient_formset,
            action_url=reverse("recipe_create"),
            cancel_url=reverse("recipe_list"),
        )

    async def post(self, request: HttpRequest) -> HttpResponse:
        if not await _user_has_any_permission(request, "recipes.add_recipe"):
            return HttpResponse(status=403)
        form, ingredient_formset = _build_recipe_forms(request)

        is_form_valid = await sync_to_async(form.is_valid)()
        is_formset_valid = await sync_to_async(ingredient_formset.is_valid)()

        if is_form_valid and is_formset_valid:
            saved_recipe = await sync_to_async(form.save)()
            ingredient_formset.instance = saved_recipe
            await sync_to_async(ingredient_formset.save)()
            return redirect("recipe_detail", recipe_id=saved_recipe.pk)

        return await _render_recipe_form(
            request,
            form=form,
            ingredient_formset=ingredient_formset,
            status=400,
            action_url=reverse("recipe_create"),
            cancel_url=reverse("recipe_list"),
        )


class RecipeDetailView(View):
    async def get(self, request: HttpRequest, recipe_id: int) -> HttpResponse:
        """Display recipe details with portions input (default=1)"""
        recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
        ingredients: list[Ingredient] = [ingredient async for ingredient in recipe.ingredients.all()]

        return await sync_to_async(render)(
            request=request,
            template_name="recipes/recipe_detail.html",
            context={"recipe": recipe, "ingredients": ingredients},
        )

    async def delete(self, request: HttpRequest, recipe_id: int) -> HttpResponse:
        """Delete recipe"""
        if not await _user_has_any_permission(request, "recipes.delete_recipe"):
            return HttpResponse(status=403)

        recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
        await recipe.adelete()
        response = redirect("recipe_list")
        response.status_code = 303
        return response


class RecipeChangeView(View):
    async def get(self, request: HttpRequest, recipe_id: int) -> HttpResponse:
        if not await _user_has_any_permission(request, "recipes.change_recipe"):
            return HttpResponse(status=403)
        recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
        form, ingredient_formset = _build_recipe_forms(request, recipe)
        return await _render_recipe_form(
            request,
            form=form,
            ingredient_formset=ingredient_formset,
            recipe=recipe,
            action_url=reverse("recipe_change", kwargs={"recipe_id": recipe_id}),
            cancel_url=reverse("recipe_detail", kwargs={"recipe_id": recipe_id}),
        )

    async def post(self, request: HttpRequest, recipe_id: int) -> HttpResponse:
        if not await _user_has_any_permission(request, "recipes.change_recipe"):
            return HttpResponse(status=403)
        recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
        form, ingredient_formset = _build_recipe_forms(request, recipe)

        is_form_valid = await sync_to_async(form.is_valid)()
        is_formset_valid = await sync_to_async(ingredient_formset.is_valid)()

        if is_form_valid and is_formset_valid:
            await sync_to_async(form.save)()
            await sync_to_async(ingredient_formset.save)()
            response = redirect("recipe_detail", recipe_id=recipe.id)
            response.status_code = 303
            return response

        return await _render_recipe_form(
            request,
            form=form,
            ingredient_formset=ingredient_formset,
            recipe=recipe,
            status=400,
            action_url=reverse("recipe_change", kwargs={"recipe_id": recipe_id}),
            cancel_url=reverse("recipe_detail", kwargs={"recipe_id": recipe_id}),
        )


@datastar_response
@require_http_methods(["GET"])
async def recipe_ingredients(request: HttpRequest, recipe_id: int) -> AsyncGenerator[Any, None]:
    """Return updated ingredients HTML based on portions parameter"""
    recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
    ingredients: list[Ingredient] = [ingredient async for ingredient in recipe.ingredients.all()]
    signals: dict[str, Any] | None = read_signals(request)
    portions = _normalize_portions(signals)

    # Calculate quantities based on portions
    calculated_ingredients: list[dict[str, Any]] = [
        {"name": ing.name, "quantity": ing.quantity * portions, "unit": ing.unit} for ing in ingredients
    ]

    rendered_html: str = render_to_string("recipes/_ingredients.html", {"ingredients": calculated_ingredients})

    yield ServerSentEventGenerator.patch_elements(rendered_html)


def _extract_formset_prefix(data: dict[str, Any]) -> str | None:
    for key in data:
        if key.endswith("-TOTAL_FORMS"):
            return key.rsplit("-", 1)[0]
    return None


@require_http_methods(["POST"])
async def add_ingredient_form(request: HttpRequest) -> HttpResponse:
    """Morph the entire ingredient section after add/remove actions."""
    if not await _user_has_any_permission(request, "recipes.add_recipe", "recipes.change_recipe"):
        return HttpResponse(status=403)
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
        recipe = await aget_object_or_404(Recipe, id=recipe_pk)

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
    ingredient_formset = await sync_to_async(
        lambda: IngredientFormSet(
            data=data,
            files=request.FILES,
            instance=formset_instance,
            prefix=prefix,
        )
    )()

    rendered_section = await sync_to_async(render_to_string)(
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
