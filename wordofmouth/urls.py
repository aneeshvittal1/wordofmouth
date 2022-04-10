from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'wordofmouth'
urlpatterns = [
    path('', views.recipe_explore, name="recipe_explore"),
    path('create', views.recipe_experiment, name="recipe_experiment"),
    path('recipe/<int:recipe_id>', views.recipe_detail, name="recipe_detail"),
    path('favorites', views.favorite_list, name="favorite_list"),
    path('wordofmouth/newrecipe', views.new_recipe, name='new_recipe'),
    path('fav/<int:recipe_id>', views.favorite_add, name='favorite_add')
]