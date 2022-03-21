from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="explore.html")),
    path('experiment', TemplateView.as_view(template_name="experiment.html")),
    path('experiment/<int:recipe_id>', views.recipe_detail, name="recipe_detail"),
]