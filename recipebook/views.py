from django.shortcuts import render
from django.http import HttpResponse
from recipebook.models import Recipe, Author
from recipebook.forms import NewRecipeAdd, NewAuthorAdd


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


def new_recipe_add(request):
    form = None
    if request.method == 'POST':
        form = NewRecipeAdd(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                author=Author.objects.filter(id=data['author']).first(),
                description=data['description'],
                time=data['time'],
                instructions=data['instructions'],
            )
            return render(request, 'success_view.html', {'data': 'Recipe'})
    else:
        form = NewRecipeAdd()
        return render(request, 'new_recipe_add.html', {'form': form})


def new_author_add(request):
    form = None
    if request.method == 'POST':
        form = NewAuthorAdd(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data['name'],
                bio=data['bio']
            )
            return render(request, 'success_view.html', {'data': 'Author'})
    else:
        form = NewAuthorAdd()
        return render(request, 'new_author_add.html', {'form': form})