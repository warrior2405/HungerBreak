from django import forms
from django.forms import ModelForm
from .models import Recipe

# Recipe Meal Planner Form
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'day_of_the_week',
            'meal_type',
            'recipe_name',
            'recipe_description',
            'ingredients',
            'preparation_steps',
            'prep_time',
            'cook_time',
            'servings',
            'nutritional_info',
            'recipe_image']
        widgets = {
            'day_of_the_week': forms.Select(),
            'meal_type': forms.Select(),
            'recipe_name': forms.TextInput(attrs={'placeholder': 'Enter recipe name'}),
            'recipe_description': forms.Textarea(attrs={'placeholder': 'Enter recipe description'}),
        }