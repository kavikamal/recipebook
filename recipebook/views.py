from django.shortcuts import render
from django.http import HttpResponse
from recipebook.models import Recipe


def recipe_view(request):
    html = """
    Hello Recipe 1
    """

    return HttpResponse(html)
