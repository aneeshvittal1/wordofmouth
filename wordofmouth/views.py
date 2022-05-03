from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from .models import Recipe
from .forms import RecipePostForm
from taggit.models import Tag
from django.db.models import Q


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

    # if request.method == 'POST':
    #     recipe.likes += 1
    #     recipe.save()

    is_liked = False
    if recipe.likes.filter(id=request.user.id).exists():
        is_liked = True
    is_favorite = False
    if recipe.favorites.filter(id=request.user.id):
        is_favorite = True

    context = {
        'recipe': recipe,
        'is_liked': is_liked,
        'total_likes': recipe.total_likes(),
        'is_favorite': is_favorite,
    }

    return render(request, 'wordofmouth/recipe_detail.html', context)

"""
*  REFERENCES
*  Title: <Learn Django - The Easy Way | Creating a Like/Dislike Button | Tutorial - 37>
*  Author: <Abhishek Verma>
*  Date: <April 4, 2018>
*  URL: <https://www.youtube.com/watch?v=VoWw1Y5qqt8>
"""

def like_recipe(request):
    recipe = get_object_or_404(Recipe, id=request.POST.get('recipe_id'))
    is_liked = False
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
        is_liked = False
    else:
        recipe.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(reverse('wordofmouth:recipe_detail', args=(recipe.id,)))


def recipe_explore(request):
    recipe_list = reversed(Recipe.objects.all())
    tags_list = Recipe.tags.most_common()[:14]
    context = {
        'recipe_list': recipe_list,
        'tags_list': tags_list,
    }
    return render(request, 'wordofmouth/recipe_explore.html', context)
    
def recipe_explore_tags(request, tag):
    try:
        recipes = Recipe.objects.filter(tags__name__in=[tag])
        num_results = len(recipes)
    except:
        raise Http404("Error: Invalid tag")
    context = {
        'recipe_list': recipes,
        'tag': tag,
        'num_results':num_results
    }
    return render(request, 'wordofmouth/recipe_explore_tags.html', context)

def recipe_experiment(request):
    return render(request, 'wordofmouth/recipe_experiment.html',{'form': RecipePostForm,'error':False})


def recipe_fork(request, fork):
    og_recipe = Recipe.objects.get(pk=fork)
    context = {
        'fork': fork,
        'form': RecipePostForm(initial={'recipe_title':og_recipe.recipe_title,'description':og_recipe.description,'ingredients':og_recipe.ingredients,'instructions':og_recipe.instructions}),
    }
    return render(request, 'wordofmouth/recipe_fork.html', context)


def new_recipe(request):
    new_r = request.POST.copy()
    new_r['tags'] = new_r['tags'].replace('#', '')
    form = RecipePostForm(new_r)
    print(request.POST)
    if form.is_valid():
        new_r = form.save(commit=False)
        new_r.pub_date = timezone.now()
        new_r.author = request.user.username
        if 'filename' not in request.FILES:
            new_r.picture="defaultRecipePic.png"
        else:
            new_r.picture=request.FILES['filename']
        new_r.save()
        form.save_m2m()
        return redirect('/wordofmouth/recipe/'+str(new_r.get_pk()))
    else:
        return render(request, 'wordofmouth/recipe_experiment.html',{'form': form, 'error': True})


"""
*  REFERENCES
*  Title: <Learn Django - The Easy Way | Adding Posts to Favourites | Tutorial - 51>
*  Author: <Abhishek Verma>
*  Date: <April 4, 2018>
*  URL: <https://www.youtube.com/watch?v=1XiJvIuvqhs>
"""

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


def recipe_search(request):
    recipe = Recipe.objects.all()
    query = request.GET.get('q')
    print(query)
    if query:
        recipe = Recipe.objects.filter(
            Q(recipe_title__icontains=query)|
            Q(ingredients__icontains=query)|
            Q(instructions__icontains=query)|
            Q(description__icontains=query)
            )
    context = {
        'recipe': recipe,
    }
    return render(request, 'wordofmouth/recipe_search.html', context )


def user_list(request):
    recipes = Recipe.objects.all()
    user = request.user
    user_recipes = []
    for each in recipes:
        if user.username == each.author:
            user_recipes.append(each)
    context = {
        'user_recipes': user_recipes,
    }
    print(user_recipes)
    return render(request, 'wordofmouth/user_recipes.html', context)


def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    if user.username != recipe.author:
        raise Http404
    recipe.delete()
    return HttpResponseRedirect(reverse('wordofmouth:user_list',))
