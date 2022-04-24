from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Recipe
from django.utils import timezone
import json
from django_quill.fields import QuillField
from .forms import RecipePostForm
from taggit.managers import TaggableManager
from django_quill.fields import QuillField

# Create your tests here.
class LoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    def test_login(self):
        # send login data
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertEquals(response.status_code, 200)

class RecipeModelTests(TestCase):
    def test_title_likes_instructions(self):
        x = {
            "delta":{
                "ops": [
                    { "insert": ' Bread and Wine ' },
                ]
            }
        }
        y = json.dumps(x)
        u = User(username="test", password="123")
        u.save()
        r = Recipe(recipe_title='Bread and Wine', pub_date=timezone.now(), instructions=y)
        r.save()
        self.assertEquals(r.recipe_title, 'Bread and Wine')
        self.assertEquals(r.instructions, y)
        r.delete()

    # def test_favorites(self):
    #     User.

    # I think im testing the many to many relationships here to see if the user is connected to the likes and favorites
    def test_favorites_has_user(self):
        u = User(username="test", password="123")
        u.save()
        r = Recipe(recipe_title='Bread and Wine', pub_date=timezone.now())
        r.save()
        r.favorites.set([u.pk])
        self.assertEqual(r.favorites.count(), 1)

    def test_like_has_user(self):
        u = User(username="test", password="123")
        u.save()
        r = Recipe(recipe_title='Bread and Wine', pub_date=timezone.now())
        r.save()
        r.likes.set([u.pk])
        self.assertEqual(r.likes.count(), 1)

    def test_quill_field_delta(self):
        x = {
            "delta":{
                "ops": [
                    { "insert": 'The Ultimate Bread and Wine Test' },
                ]
            }
        }
        x = json.dumps(x)
        r = Recipe(recipe_title='Bread and Wine', pub_date=timezone.now(), instructions = x)
        y = {
            "delta":{
                "ops": [
                    { "insert": 'The Ultimate Bread and Wine Test' },
                ]
            }
        }
        y = json.dumps(y)
        self.assertEqual(r.instructions,y)

class RecipeFormTest(TestCase):
    def test_form_valid_with_required_fields_filled(self):
        x = {
            "delta":{
                "ops": [
                    { "insert": ' Bread and Wine ' },
                ]
            }
        }
        y = json.dumps(x)
        r = {'is_forked': 0, 'forked_id': 0, 'recipe_title': ['Hello'], 'description': ['d'], 'ingredients': y, 'instructions': y, 'tags': ['test']}
        form = RecipePostForm(r)
        self.assertTrue(form.is_valid())
    
    def test_form_requires_title(self):
        x = {
            "delta":{
                "ops": [
                    { "insert": ' Bread and Wine ' },
                ]
            }
        }
        y = json.dumps(x)
        r = {'is_forked': 0, 'forked_id': 0, 'description': ['d'], 'ingredients': y, 'instructions': y, 'tags': ['test']}
        form = RecipePostForm(r)
        self.assertFalse(form.is_valid())
    
    def test_form_requires_ingredients(self):
        x = {
            "delta":{
                "ops": [
                    { "insert": ' Bread and Wine ' },
                ]
            }
        }
        y = json.dumps(x)
        r = {'is_forked': 0, 'forked_id': 0, 'recipe_title': ['Hello'], 'description': ['d'], 'instructions': y, 'tags': ['test']}
        form = RecipePostForm(r)
        self.assertFalse(form.is_valid())

    def test_form_requires_instructions(self):
        x = {
            "delta":{
                "ops": [
                    { "insert": ' Bread and Wine ' },
                ]
            }
        }
        y = json.dumps(x)
        r = {'is_forked': 0, 'forked_id': 0, 'recipe_title': ['Hello'], 'description': ['d'], 'ingredients': y, 'tags': ['test']}
        form = RecipePostForm(r)
        self.assertFalse(form.is_valid())

    def test_form_requires_min_one_tag(self):
        x = {
            "delta":{
                "ops": [
                    { "insert": ' Bread and Wine ' },
                ]
            }
        }
        y = json.dumps(x)
        r = {'is_forked': 0, 'forked_id': 0, 'recipe_title': ['Hello'], 'description': ['d'], 'ingredients': y, 'instructions': y, 'tags': []}
        form = RecipePostForm(r)
        self.assertFalse(form.is_valid()) 

    def test_form_description_optional(self):
        x = {
            "delta":{
                "ops": [
                    { "insert": ' Bread and Wine ' },
                ]
            }
        }
        y = json.dumps(x)
        r = {'is_forked': 0, 'forked_id': 0, 'recipe_title': ['Hello'], 'ingredients': y, 'instructions': y, 'tags': ['test']}
        form = RecipePostForm(r)
        self.assertTrue(form.is_valid())