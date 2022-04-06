from django import forms
from .models import Recipe
from taggit.forms import TagWidget


class RecipePostForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = (
            'recipe_title','instructions','description','tags',
           
        )
        exclude = (
            'author','pub_date','likes','picture'
        )
        widgets = {
            'tags':TagWidget(),
        }


