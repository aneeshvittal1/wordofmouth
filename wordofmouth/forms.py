from django import forms
from .models import Recipe
from taggit.forms import TagWidget


class RecipePostForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = (
            'recipe_title','instructions','description','tags','is_forked','forked_id'
           
        )
        exclude = (
            'author','pub_date','likes','picture'
        )
        widgets = {
            'tags':TagWidget(),
        }


