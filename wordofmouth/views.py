from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from .models import Recipe


def index(request):
    return HttpResponse("Hello, world. You're at the word of mouth index.")

def recipe_detail(request, recipe_id):
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
        # recipe = Recipe.objects.all()[recipe_id-1]
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")
    return render(request, 'wordofmouth/detail.html', {'recipe': recipe})