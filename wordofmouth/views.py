from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from .models import Recipe
from .forms import RecipePostForm


def index(request):
    return HttpResponse("Hello, world. You're at the word of mouth index.")
    # return render(request, 'wordofmouth/recipe_detail.html', {
    #     "recipes": Recipe.objects.all(),
    #     "likes": Like.objects.all(),
    # })


def recipe_detail(request, recipe_id):
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
        # recipe = Recipe.objects.all()[recipe_id-1]
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")
    #recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        recipe.likes += 1
        recipe.save()

    return render(request, 'wordofmouth/recipe_detail.html', {'recipe': recipe})

def recipe_explore(request):
    recipe_list = Recipe.objects.all()
    context = {
        'recipe_list': recipe_list,
    }
    print(recipe_list)
    return render(request, 'wordofmouth/recipe_explore.html', context)

def recipe_experiment(request):
    return render(request, 'wordofmouth/recipe_experiment.html',{'form': RecipePostForm})

def new_recipe(request):
    r = Recipe(recipe_title=request.POST['recipe_title'],description=request.POST['description'], likes=0, pub_date=timezone.now(), instructions=request.POST['instructions'], picture=request.FILES['filename'], author=request.user.username)
    r.save()
    return redirect('/wordofmouth/recipe/'+str(r.pk))


@login_required
def favorite_add(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    fav_list = []
    if recipe.favorites.filter(id=request.user.recipe_id).exists():
        recipe.favorites.remove(request.user)
        fav_list.remove(recipe)
    else:
        recipe.favorites.add(request.user)
        fav_list.append(recipe)
    context = {
        'fav_list': fav_list
    }
    print(fav_list)
    return render(request, 'wordofmouth/favorites.html', {'context': context})


@login_required
def favorite_list(request):
    new = Recipe.objects.filter(favorites=request.user)
    return render(request, 'wordofmouth/favorites.html', {'new': new})

   

