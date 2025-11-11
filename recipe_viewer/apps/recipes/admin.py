from django.contrib import admin

from recipe_viewer.apps.recipes.models import Ingredient
from recipe_viewer.apps.recipes.models import Recipe


class IngredientInline(admin.TabularInline):
    """Inline admin for ingredients to be added directly in recipe form"""

    model = Ingredient
    extra = 3  # Show 3 empty ingredient forms by default
    fields = ["name", "quantity", "unit"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin interface for Recipe model"""

    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name", "steps"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = [
        ("Basic Information", {"fields": ["name", "image"]}),
        ("Instructions", {"fields": ["steps"]}),
        ("Metadata", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]

    inlines = [IngredientInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Admin interface for Ingredient model (standalone)"""

    list_display = ["name", "quantity", "unit", "recipe"]
    search_fields = ["name", "recipe__name"]
    list_filter = ["recipe"]
