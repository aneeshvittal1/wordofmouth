from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Recipe
from django.utils import timezone

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
        r = Recipe(recipe_title='Bread and Wine', likes=12, pub_date=timezone.now(), instructions='get bread and wine')
        r.save()
        self.assertEquals(r.recipe_title, 'Bread and Wine')
        self.assertEquals(r.likes, 12)
        self.assertEquals(r.instructions, 'get bread and wine')
        r.delete()