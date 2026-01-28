import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from recipe_viewer.apps.recipes.models import Ingredient
from recipe_viewer.apps.recipes.models import Recipe


class Command(BaseCommand):
    """
    Wipes the database and imports recipes from a JSON file.
    The JSON file is expected to be in the following format:
    [
        {
            "name": "recipe_name",
            "steps": [
            "step_1",
            "step_2",
            "step_3"
            ],
            "ingredients": [
            {
                "name": "ingredient_name_1",
                "quantity": 10.0,
                "unit": "dag",
            },
            {
                "name": "ingredient_name_2",
                "quantity": 0.5,
                "unit": "l",
            }
            ]
        }
    ]
    """

    help = "Wipe recipes and import from JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default="recipes_dbf.json",
            help="Path to JSON file (default: recipes_dbf.json)",
        )

    @transaction.atomic
    def handle(self, *args, **options):  # noqa: ARG002
        json_path = Path(options["path"])
        if not json_path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {json_path}"))
            return

        self.stdout.write("Clearing existing recipes and ingredients...")
        Recipe.objects.all().delete()

        self.stdout.write(f"Loading recipes from {json_path}...")
        data = json.loads(json_path.read_text(encoding="utf-8"))

        recipe_count = 0
        ingredient_count = 0

        for entry in data:
            steps = entry.get("steps") or []
            steps_text = "\n".join(steps) if isinstance(steps, list) else str(steps)

            recipe = Recipe.objects.create(
                name=entry.get("name", "").strip(),
                steps=steps_text,
            )
            recipe_count += 1

            ingredients = entry.get("ingredients") or []
            for ingredient in ingredients:
                Ingredient.objects.create(
                    recipe=recipe,
                    name=str(ingredient.get("name", "")).strip(),
                    quantity=float(ingredient.get("quantity") or 0.0),
                    unit=str(ingredient.get("unit", "")).strip(),
                )
                ingredient_count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {recipe_count} recipes and {ingredient_count} ingredients."))
