from django.db import models


class Ingredient(models.Model):
    """Model representing an ingredient"""
    name = models.CharField(max_length=255)
    quantity = models.FloatField()
    unit = models.CharField(max_length=255)

    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.name}"    

class Recipe(models.Model):
    """Model representing a recipe"""
    name = models.CharField(max_length=255)
    steps = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)

    def __str__(self):
        return self.name
