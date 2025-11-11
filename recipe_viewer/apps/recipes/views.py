from collections.abc import AsyncGenerator
from typing import Any

from datastar_py.django import ServerSentEventGenerator
from datastar_py.django import datastar_response
from datastar_py.django import read_signals
from django.conf import settings
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import aget_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import translation

from recipe_viewer.apps.recipes.models import Ingredient
from recipe_viewer.apps.recipes.models import Recipe


async def recipe_list(request: HttpRequest) -> HttpResponse:
    """Display list of all recipes"""
    recipes: list[Recipe] = [recipe async for recipe in Recipe.objects.all().order_by("-created_at")]
    return render(request, "recipes/recipe_list.html", {"recipes": recipes})


async def recipe_detail(request: HttpRequest, recipe_id: int) -> HttpResponse:
    """Display recipe details with portions input (default=1)"""
    recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
    ingredients: list[Ingredient] = [ingredient async for ingredient in recipe.ingredients.all()]

    return render(
        request,
        "recipes/recipe_detail.html",
        {
            "recipe": recipe,
            "ingredients": ingredients,
        },
    )


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
