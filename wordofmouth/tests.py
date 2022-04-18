from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Recipe
from django.utils import timezone
import json

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
