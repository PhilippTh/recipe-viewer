from collections.abc import AsyncGenerator
from typing import Any

from datastar_py.django import ServerSentEventGenerator
from datastar_py.django import datastar_response
from datastar_py.django import read_signals
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import aget_object_or_404
from django.shortcuts import render
from django.template.loader import render_to_string

from recipe_viewer.apps.recipes.models import Ingredient
from recipe_viewer.apps.recipes.models import Recipe


async def recipe_list(request: HttpRequest) -> HttpResponse:
    """Display list of all recipes"""
    recipes: list[Recipe] = [recipe async for recipe in Recipe.objects.all().order_by("-created_at")]
    return render(request, "recipes/recipe_list.html", {"recipes": recipes})


async def recipe_detail(request: HttpRequest, recipe_id: int) -> HttpResponse:
    """Display recipe details with serving size input (default=1)"""
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
    """Return updated ingredients HTML based on serving_size parameter"""
    recipe: Recipe = await aget_object_or_404(Recipe, id=recipe_id)
    ingredients: list[Ingredient] = [ingredient async for ingredient in recipe.ingredients.all()]
    signals: dict[str, Any] | None = read_signals(request)

    if signals is None:
        signals = {}

    # Calculate quantities based on serving size
    calculated_ingredients: list[dict[str, Any]] = [
        {"name": ing.name, "quantity": ing.quantity * signals["serving_size"], "unit": ing.unit} for ing in ingredients
    ]

    rendered_html: str = render_to_string("recipes/_ingredients.html", {"ingredients": calculated_ingredients})

    yield ServerSentEventGenerator.patch_elements(rendered_html)
