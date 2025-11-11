from django.shortcuts import render
from django.shortcuts import aget_object_or_404
from recipe_viewer.apps.recipes.models import Recipe
from django.template.loader import render_to_string
from datastar_py.django import ServerSentEventGenerator as SSE
from datastar_py.django import datastar_response
from datastar_py.django import read_signals


async def recipe_list(request):
    """Display list of all recipes"""
    recipes = [recipe async for recipe in Recipe.objects.all().order_by('-created_at')]
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


async def recipe_detail(request, recipe_id):
    """Display recipe details with serving size input (default=1)"""
    recipe = await aget_object_or_404(Recipe, id=recipe_id)
    ingredients = [ingredient async for ingredient in recipe.ingredients.all()]
    
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'ingredients': ingredients,
    })


@datastar_response
async def recipe_ingredients(request, recipe_id):
    """Return updated ingredients HTML based on serving_size parameter"""
    recipe = await aget_object_or_404(Recipe, id=recipe_id)
    ingredients = [ingredient async for ingredient in recipe.ingredients.all()]
    signals = read_signals(request)
    
    # Calculate quantities based on serving size
    calculated_ingredients = [
        {
            'name': ing.name,
            'quantity': ing.quantity * signals['serving_size'],
            'unit': ing.unit
        }
        for ing in ingredients
    ]

    rendered_html = render_to_string('recipes/_ingredients.html', {
        'ingredients': calculated_ingredients
    })
    
    yield SSE.patch_elements(rendered_html)
