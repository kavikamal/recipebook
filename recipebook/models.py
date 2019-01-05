from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=500)


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,)
    description = models.CharField(max_length=300)
    time = models.IntegerField(default=0)
    instructions = models.TextField(max_length=5000)
