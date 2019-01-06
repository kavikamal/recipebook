from django.shortcuts import render
from django.http import HttpResponse
from recipebook.models import Recipe, Author


def home_view(request):
    data = Recipe.objects.all()
    return render(request, 'home_view.html', {'data': data})


def recipe_view(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    return render(request, 'recipe_view.html', {'data': recipe})


def author_view(request, author_id):
    data = {
        'author': Author.objects.get(pk=author_id),
        'recipes': list(Recipe.objects.all().filter(
            author__id=author_id).values()
        )
    }
    return render(request, 'author_view.html', {'data': data})
