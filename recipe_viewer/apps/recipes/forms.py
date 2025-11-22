from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from recipe_viewer.apps.recipes.models import Ingredient
from recipe_viewer.apps.recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    """Form for creating and editing recipes"""

    use_required_attribute = False

    class Meta:
        model = Recipe
        fields = ["name", "steps", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": (
                        "text-2xl font-bold text-slate-800 bg-transparent border-none "
                        "focus:outline-none focus:ring-0 mb-1"
                    ),
                    "placeholder": _("Recipe name..."),
                }
            ),
            "steps": forms.Textarea(
                attrs={
                    "class": (
                        "w-full bg-gray-50 rounded-lg p-3 border border-gray-200 focus:border-blue-400 "
                        "focus:ring-2 focus:ring-blue-200 focus:outline-none transition-all text-sm leading-normal "
                        "resize-y min-h-[300px] whitespace-pre-wrap"
                    ),
                    "rows": 12,
                    "placeholder": _("Enter step-by-step instructions..."),
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": (
                        "block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md "
                        "file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 "
                        "hover:file:bg-blue-100"
                    ),
                }
            ),
        }


class IngredientForm(forms.ModelForm):
    """Form for creating and editing ingredients"""

    use_required_attribute = False

    class Meta:
        model = Ingredient
        fields = ["quantity", "unit", "name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": (
                        "w-full px-2 py-1 bg-white border border-gray-300 rounded text-sm focus:border-blue-400 "
                        "focus:ring-1 focus:ring-blue-200 focus:outline-none transition-all"
                    ),
                    "placeholder": _("Ingredient name"),
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": (
                        "w-full px-2 py-1 bg-white border border-gray-300 rounded text-sm focus:border-blue-400 "
                        "focus:ring-1 focus:ring-blue-200 focus:outline-none transition-all"
                    ),
                    "placeholder": "0",
                    "step": "0.01",
                }
            ),
            "unit": forms.TextInput(
                attrs={
                    "class": (
                        "w-full px-2 py-1 bg-white border border-gray-300 rounded text-sm focus:border-blue-400 "
                        "focus:ring-1 focus:ring-blue-200 focus:outline-none transition-all"
                    ),
                    "placeholder": _("Unit"),
                }
            ),
        }


# Inline formset for managing ingredients within a recipe form
IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=0,  # Number of additional empty forms to display
    can_delete=True,
    min_num=1,  # Require at least one ingredient
    validate_min=True,
)
