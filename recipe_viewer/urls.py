"""
URL configuration for recipe_viewer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from recipe_viewer.apps.recipes.views import RecipeDetailView
from recipe_viewer.apps.recipes.views import edit_recipe
from recipe_viewer.apps.recipes.views import recipe_ingredients
from recipe_viewer.apps.recipes.views import recipe_list
from recipe_viewer.apps.recipes.views import set_language

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", recipe_list, name="recipe_list"),
    path("recipe/<int:recipe_id>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("recipe/<int:recipe_id>/edit/", edit_recipe, name="recipe_edit"),
    path("recipe/<int:recipe_id>/ingredients/", recipe_ingredients, name="recipe_ingredients"), # type: ignore[arg-type]
    path("set_language/", set_language, name="set_language"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
