from django.core.management.base import BaseCommand

from recipe_viewer.apps.recipes.models import Ingredient
from recipe_viewer.apps.recipes.models import Recipe


class Command(BaseCommand):
    help = "Populates the database with sample recipe data"

    def handle(self, *args, **kwargs):  # noqa: ARG002
        # Clear existing data
        self.stdout.write("Clearing existing recipes and ingredients...")
        Recipe.objects.all().delete()

        # Create recipes with ingredients
        self.stdout.write("Creating sample recipes...")

        # Recipe 1: Chocolate Chip Cookies
        recipe1 = Recipe.objects.create(
            name="Chocolate Chip Cookies",
            steps="""1. Preheat oven to 375°F (190°C).
2. In a large bowl, cream together butter and sugars until fluffy.
3. Beat in eggs and vanilla extract.
4. In a separate bowl, combine flour, baking soda, and salt.
5. Gradually blend dry ingredients into wet ingredients.
6. Stir in chocolate chips.
7. Drop spoonfuls of dough onto ungreased cookie sheets.
8. Bake for 9-11 minutes or until golden brown.
9. Cool on baking sheet for 2 minutes before removing to a wire rack.""",
        )

        Ingredient.objects.create(recipe=recipe1, name="all-purpose flour", quantity=2.25, unit="cups")
        Ingredient.objects.create(recipe=recipe1, name="baking soda", quantity=1, unit="tsp")
        Ingredient.objects.create(recipe=recipe1, name="salt", quantity=1, unit="tsp")
        Ingredient.objects.create(recipe=recipe1, name="butter, softened", quantity=1, unit="cup")
        Ingredient.objects.create(recipe=recipe1, name="granulated sugar", quantity=0.75, unit="cup")
        Ingredient.objects.create(recipe=recipe1, name="brown sugar", quantity=0.75, unit="cup")
        Ingredient.objects.create(recipe=recipe1, name="eggs", quantity=2, unit="large")
        Ingredient.objects.create(recipe=recipe1, name="vanilla extract", quantity=2, unit="tsp")
        Ingredient.objects.create(recipe=recipe1, name="chocolate chips", quantity=2, unit="cups")

        self.stdout.write(self.style.SUCCESS(f"✓ Created: {recipe1.name}"))

        # Recipe 2: Classic Spaghetti Carbonara
        recipe2 = Recipe.objects.create(
            name="Classic Spaghetti Carbonara",
            steps="""1. Bring a large pot of salted water to boil. Cook spaghetti according to package directions.
2. While pasta cooks, fry pancetta in a large skillet until crispy.
3. In a bowl, whisk together eggs, Parmesan cheese, and black pepper.
4. Reserve 1 cup of pasta water, then drain the spaghetti.
5. Add hot pasta to the skillet with pancetta and toss.
6. Remove from heat and quickly stir in egg mixture, adding pasta water as needed to create a creamy sauce.
7. Serve immediately with extra Parmesan and black pepper.""",
        )

        Ingredient.objects.create(recipe=recipe2, name="spaghetti", quantity=400, unit="g")
        Ingredient.objects.create(recipe=recipe2, name="pancetta, diced", quantity=200, unit="g")
        Ingredient.objects.create(recipe=recipe2, name="eggs", quantity=4, unit="large")
        Ingredient.objects.create(recipe=recipe2, name="Parmesan cheese, grated", quantity=1, unit="cup")
        Ingredient.objects.create(recipe=recipe2, name="black pepper", quantity=1, unit="tsp")
        Ingredient.objects.create(recipe=recipe2, name="salt", quantity=1, unit="pinch")

        self.stdout.write(self.style.SUCCESS(f"✓ Created: {recipe2.name}"))

        # Recipe 3: Chicken Stir-Fry
        recipe3 = Recipe.objects.create(
            name="Quick Chicken Stir-Fry",
            steps="""1. Cut chicken into bite-sized pieces and season with salt and pepper.
2. Heat oil in a large wok or skillet over high heat.
3. Add chicken and stir-fry for 5-6 minutes until cooked through. Remove and set aside.
4. Add more oil if needed, then stir-fry vegetables for 3-4 minutes.
5. Return chicken to the pan.
6. Mix soy sauce, garlic, and ginger, then pour over chicken and vegetables.
7. Toss everything together and cook for 2 more minutes.
8. Serve hot over rice.""",
        )

        Ingredient.objects.create(recipe=recipe3, name="chicken breast, sliced", quantity=500, unit="g")
        Ingredient.objects.create(recipe=recipe3, name="bell peppers, sliced", quantity=2, unit="medium")
        Ingredient.objects.create(recipe=recipe3, name="broccoli florets", quantity=1, unit="cup")
        Ingredient.objects.create(recipe=recipe3, name="soy sauce", quantity=3, unit="tbsp")
        Ingredient.objects.create(recipe=recipe3, name="garlic, minced", quantity=2, unit="cloves")
        Ingredient.objects.create(recipe=recipe3, name="fresh ginger, grated", quantity=1, unit="tsp")
        Ingredient.objects.create(recipe=recipe3, name="vegetable oil", quantity=2, unit="tbsp")

        self.stdout.write(self.style.SUCCESS(f"✓ Created: {recipe3.name}"))

        # Recipe 4: Pancakes
        recipe4 = Recipe.objects.create(
            name="Fluffy Pancakes",
            steps="""1. In a large bowl, sift together flour, baking powder, salt, and sugar.
2. Make a well in the center and pour in milk, egg, and melted butter.
3. Mix until smooth (a few lumps are okay).
4. Heat a lightly oiled griddle or frying pan over medium-high heat.
5. Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake.
6. Cook until bubbles form on the surface, then flip and cook until golden brown on the other side.
7. Serve hot with butter and maple syrup.""",
        )

        Ingredient.objects.create(recipe=recipe4, name="all-purpose flour", quantity=1.5, unit="cups")
        Ingredient.objects.create(recipe=recipe4, name="baking powder", quantity=3.5, unit="tsp")
        Ingredient.objects.create(recipe=recipe4, name="salt", quantity=1, unit="tsp")
        Ingredient.objects.create(recipe=recipe4, name="sugar", quantity=1, unit="tbsp")
        Ingredient.objects.create(recipe=recipe4, name="milk", quantity=1.25, unit="cups")
        Ingredient.objects.create(recipe=recipe4, name="egg", quantity=1, unit="large")
        Ingredient.objects.create(recipe=recipe4, name="butter, melted", quantity=3, unit="tbsp")

        self.stdout.write(self.style.SUCCESS(f"✓ Created: {recipe4.name}"))

        # Recipe 5: Guacamole
        recipe5 = Recipe.objects.create(
            name="Fresh Guacamole",
            steps="""1. Cut avocados in half, remove pit, and scoop out flesh into a bowl.
2. Mash avocados with a fork to desired consistency.
3. Add lime juice, salt, and mix well.
4. Fold in diced onion, tomatoes, cilantro, and jalapeño.
5. Taste and adjust seasonings as needed.
6. Serve immediately with tortilla chips.""",
        )

        Ingredient.objects.create(recipe=recipe5, name="ripe avocados", quantity=3, unit="large")
        Ingredient.objects.create(recipe=recipe5, name="lime juice", quantity=2, unit="tbsp")
        Ingredient.objects.create(recipe=recipe5, name="salt", quantity=0.5, unit="tsp")
        Ingredient.objects.create(recipe=recipe5, name="red onion, diced", quantity=0.25, unit="cup")
        Ingredient.objects.create(recipe=recipe5, name="tomatoes, diced", quantity=2, unit="small")
        Ingredient.objects.create(recipe=recipe5, name="fresh cilantro, chopped", quantity=2, unit="tbsp")
        Ingredient.objects.create(recipe=recipe5, name="jalapeño, minced", quantity=1, unit="small")

        self.stdout.write(self.style.SUCCESS(f"✓ Created: {recipe5.name}"))

        # Recipe 6: Caesar Salad
        recipe6 = Recipe.objects.create(
            name="Caesar Salad",
            steps="""1. Wash and dry romaine lettuce, then tear into bite-sized pieces.
2. In a small bowl, whisk together mayonnaise, lemon juice, Worcestershire sauce, Dijon mustard, and minced garlic.
3. Add anchovy paste if desired and mix well.
4. Season with salt and pepper.
5. Place lettuce in a large bowl and add croutons.
6. Drizzle with dressing and toss to coat.
7. Sprinkle with Parmesan cheese and serve immediately.""",
        )

        Ingredient.objects.create(recipe=recipe6, name="romaine lettuce", quantity=1, unit="head")
        Ingredient.objects.create(recipe=recipe6, name="mayonnaise", quantity=0.5, unit="cup")
        Ingredient.objects.create(recipe=recipe6, name="lemon juice", quantity=2, unit="tbsp")
        Ingredient.objects.create(recipe=recipe6, name="Worcestershire sauce", quantity=1, unit="tsp")
        Ingredient.objects.create(recipe=recipe6, name="Dijon mustard", quantity=1, unit="tsp")
        Ingredient.objects.create(recipe=recipe6, name="garlic, minced", quantity=2, unit="cloves")
        Ingredient.objects.create(recipe=recipe6, name="Parmesan cheese, shaved", quantity=0.5, unit="cup")
        Ingredient.objects.create(recipe=recipe6, name="croutons", quantity=1, unit="cup")

        self.stdout.write(self.style.SUCCESS(f"✓ Created: {recipe6.name}"))

        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Successfully created {Recipe.objects.count()} recipes with ingredients!")
        )
