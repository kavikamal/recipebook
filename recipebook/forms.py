from django import forms
from recipebook.models import Author


class NewRecipeAdd(forms.Form):
    title = forms.CharField(max_length=100)
    authors = [(a.id, a.name) for a in Author.objects.all()]
    author = forms.ChoiceField(choices=authors)
    description = forms.CharField(max_length=300)
    time = forms.IntegerField(default=0)
    instructions = forms.CharField(widget=forms.Textarea)
