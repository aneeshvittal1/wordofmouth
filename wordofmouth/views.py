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

    is_favorite = False
    if recipe.favorites.filter(id=request.user.id):
        is_favorite = True

    context = {
        'recipe': recipe,
        'is_favorite': is_favorite,
    }

    return render(request, 'wordofmouth/recipe_detail.html', context)

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


def favorite_list(request):
    user = request.user
    favorite_recipes = user.favorite.all()
    context = {
        'favorite_recipes': favorite_recipes,
    }

    return render(request, 'wordofmouth/favorites.html', context)



def favorite_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.favorites.filter(id=request.user.id).exists():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)

    return HttpResponseRedirect(reverse('wordofmouth:recipe_detail', args=(recipe.id,)))




   

