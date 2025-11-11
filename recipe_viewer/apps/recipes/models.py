from django.db import models
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    """Model representing an ingredient"""

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    quantity = models.FloatField(verbose_name=_("Quantity"))
    unit = models.CharField(max_length=255, verbose_name=_("Unit"))

    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="ingredients", verbose_name=_("Recipe"))

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")

    def __str__(self) -> str:
        # Note: Using % formatting for better translation extraction
        return _("%(quantity)s %(unit)s of %(name)s") % {
            "quantity": self.quantity,
            "unit": self.unit,
            "name": self.name,
        }


class Recipe(models.Model):
    """Model representing a recipe"""

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    steps = models.TextField(verbose_name=_("Steps"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    image = models.ImageField(upload_to="recipes/", null=True, blank=True, verbose_name=_("Image"))

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")

    def __str__(self) -> str:
        return self.name
