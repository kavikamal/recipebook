from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import reverse
from recipebook.models import Recipe, Author
from recipebook.forms import NewRecipeAdd, NewAuthorAdd, LoginForm, SignupForm


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


@login_required
def new_recipe_add(request):
    form = None
    if request.method == 'POST':
        form = NewRecipeAdd(request.user, request.POST)
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


@staff_member_required()
def new_author_add(request):
    form = None
    if request.method == 'POST':
        form = NewAuthorAdd(request.user, request.POST)
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


def signup_user(request):
    form = SignupForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password']
        )
        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, 'signup.html', {'form': form})


def login_user(request):
    next_page = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user is not None:
                login(request, user)
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponseRedirect(reverse('homepage'))
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'next': next_page})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
