from collections.abc import Callable
from typing import cast

from django.http import HttpResponseBase
from django.urls import path

from recipe_viewer.apps.recipes.views import RecipeChangeView
from recipe_viewer.apps.recipes.views import RecipeCreateView
from recipe_viewer.apps.recipes.views import RecipeDetailView
from recipe_viewer.apps.recipes.views import add_ingredient_form
from recipe_viewer.apps.recipes.views import recipe_ingredients

recipe_ingredients_view = cast(Callable[..., HttpResponseBase], recipe_ingredients)

urlpatterns = [
    path("create/", RecipeCreateView.as_view(), name="recipe_create"),
    path("create/add-ingredient-form/", add_ingredient_form, name="add_ingredient_form"),
    path("<int:recipe_id>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("<int:recipe_id>/change/", RecipeChangeView.as_view(), name="recipe_change"),
    path("<int:recipe_id>/ingredients/", recipe_ingredients_view, name="recipe_ingredients"),
]
