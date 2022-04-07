from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'wordofmouth'
urlpatterns = [
    path('', views.recipe_explore, name="recipe_explore"),
    path('create', views.recipe_experiment, name="recipe_experiment"),
    path('create/fork/<int:fork>', views.recipe_fork, name="recipe_fork"),
    path('recipe/<int:recipe_id>', views.recipe_detail, name="recipe_detail"),
    path('wordofmouth/newrecipe', views.new_recipe, name='new_recipe')
]