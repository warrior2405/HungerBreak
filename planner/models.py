from django.db import models
from django.contrib.auth.models import User

# Recipe Model
class Recipe(models.Model):
    class Weekday(models.IntegerChoices):
        Monday = 1
        Tuesday = 2
        Wednesday = 3
        Thursday = 4
        Friday = 5
        Saturday = 6
        Sunday = 7
    day_of_the_week = models.IntegerField(choices=Weekday.choices)

    def get_weekday_label(self):
        return self.Weekday(self.day_of_the_week).label

    class MealType(models.IntegerChoices):
        Breakfast = 1
        Lunch = 2
        Dinner = 3
    meal_type = models.IntegerField(choices=MealType.choices)

    def get_meal_type_label(self):
        return self.MealType(self.meal_type).label

    recipe_name = models.CharField(max_length=255)
    recipe_description = models.CharField(max_length=255)
    ingredients = models.TextField(help_text="List of ingredients separated by commas or lines",blank=True,null=True)
    preparation_steps = models.TextField(help_text="Step-by-step instructions for preparation",blank=True,null=True)
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes",default=0)
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes",default=0)
    servings = models.PositiveIntegerField(help_text="Number of servings",default=0)
    nutritional_info = models.TextField(help_text="Optional nutritional details",blank=True, null=True)
    recipe_image = models.ImageField(upload_to='recipes/', blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.get_weekday_label()} - {self.get_meal_type_label()} - {self.recipe_name}"