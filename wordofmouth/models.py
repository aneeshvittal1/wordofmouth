from urllib import request

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import auth

# Create your models here.


# class User(AbstractUser):
#     pass


class Recipe(models.Model):
    # fields
    recipe_title = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    instructions = models.TextField(blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    # user_likes = models.ManyToManyField(User)

    # __str__() method to easily see the title
    def __str__(self):
        return self.recipe_title


class Like(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipes")
    already_liked = models.BooleanField(default=False)

    def __str__(self):
        return f"you liked {self.recipe}"
