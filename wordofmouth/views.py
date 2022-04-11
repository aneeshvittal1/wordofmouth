from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from .models import Recipe
from .forms import RecipePostForm
from taggit.models import Tag


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
    return render(request, 'wordofmouth/recipe_experiment.html',{'form': RecipePostForm})


def recipe_fork(request, fork):
    og_recipe = Recipe.objects.get(pk=fork)
    context = {
        'fork': fork,
        'form': RecipePostForm(initial={'recipe_title':og_recipe.recipe_title,'description':og_recipe.description,'instructions':og_recipe.instructions}),
    }
    return render(request, 'wordofmouth/recipe_fork.html', context)


def new_recipe(request):
    form = RecipePostForm(request.POST)
    print(request.POST)
    if form.is_valid():
        new_r = form.save(commit=False)
        new_r.pub_date = timezone.now()
        new_r.author = request.user.username
        new_r.likes = 0
        new_r.picture=request.FILES['filename']
        new_r.save()
        form.save_m2m()
        return redirect('/wordofmouth/recipe/'+str(new_r.get_pk()))
    else:
        return HttpResponse('<h1>Something went wrong...</h1>')

   

