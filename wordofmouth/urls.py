from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'wordofmouth'
urlpatterns = [
    path('', views.recipe_explore, name="recipe_explore"),
    path('tags/<str:tag>', views.recipe_explore_tags, name="recipe_detail"),
    path('create', views.recipe_experiment, name="recipe_experiment"),
    path('create/fork/<int:fork>', views.recipe_fork, name="recipe_fork"),
    path('recipe/<int:recipe_id>', views.recipe_detail, name="recipe_detail"),
    path('favorite_recipe/<int:recipe_id>', views.favorite_recipe, name="favorite_recipe"),
    path('favorites', views.favorite_list, name="favorite_list"),
    path('wordofmouth/newrecipe', views.new_recipe, name='new_recipe'),
    path('like', views.like_recipe, name='like_recipe'),
    path('recipe_search', views.recipe_search, name='recipe_search'),
    path('recipe_delete/<int:recipe_id>', views.recipe_delete, name="recipe_delete"),
    path('profile', views.user_list, name='user_list'),
]


 