from django import forms
from .models import Recipe

class RecipePostForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'recipe_title','pub_date','instructions','picture'
        )