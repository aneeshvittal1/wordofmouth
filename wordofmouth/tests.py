from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Recipe
from django.utils import timezone
import json
from django_quill.fields import QuillField
from .forms import RecipePostForm
from taggit.managers import TaggableManager
from django_quill.fields import QuillField
from django.urls import reverse


# ------------------------------------------------------------ #

def create_recipe(title):
    """ 
    Helper function to create recipe for testing
    
    :param title: title of the recipe
    :return: recipe model with a few default values
    """
    return Recipe.objects.create(recipe_title=title, pub_date=timezone.now(), picture="defaultRecipePic.png")

# ------------------------------------------------------------ #

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

# ------------------------------------------------------------ #

class RecipeDetailViewTest(TestCase):
    """
    Tests for the recipe_detail view
    """

    def test_existent_recipe(self):
        """
        Basic test for a recipe that does exist
        
        We want to test is the recipe_detial view return the correct recipe
        """

        test_recipe = create_recipe("test recipe")

        url = reverse('wordofmouth:recipe_detail', args=(test_recipe.id,))
        response = self.client.get(url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, test_recipe.recipe_title)
        self.assertContains(response, test_recipe.id)
        self.assertTemplateUsed(response, 'wordofmouth/recipe_detail.html')

    def test_nonexistent_recipe(self):
        """
        Test for a recipe that does not exist
        
        This test makes sure the recipe_detail view returns a 404 if the recipe does not exist
        """

        test_id = 999999 # I'm assuming we won't have this many recipes

        url = reverse('wordofmouth:recipe_detail', args=(test_id,))
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 404)

# ------------------------------------------------------------ #

class RecipeExploreViewTest(TestCase):
    """
    Tests for recipe_explore view
    """
    def test_recipe_explore_functionality(self):
        """
        Test the recipe_explore view uses correct template
        """

        url = reverse('wordofmouth:recipe_explore')
        response = self.client.get(url, follow=True)

        self.assertTemplateUsed(response, 'wordofmouth/recipe_explore.html')

# ------------------------------------------------------------ #

class RecipeExperimentViewTest(TestCase):
    """
    Tests for recipe_experiment view
    """
    def test_recipe_experiment_functionality(self):
        """
        Test the recipe_experiment view uses correct template
        """

        url = reverse('wordofmouth:recipe_experiment')
        response = self.client.get(url, follow=True)

        self.assertTemplateUsed(response, 'wordofmouth/recipe_experiment.html')

# ------------------------------------------------------------ #

class RecipeForkViewTest(TestCase):
    """
    Tests the recipe_fork view
    """
    def test_recipe_fork_functionality(self):
        """
        Test the recipe_fork view uses correct template
        """
        og_recipe = create_recipe("test recipe")

        url = reverse('wordofmouth:recipe_fork', args=(og_recipe.id,))
        response = self.client.get(url, follow=True)

        self.assertTemplateUsed(response, 'wordofmouth/recipe_fork.html')

# ------------------------------------------------------------ #

# class NewRecipeViewTest(TestCase):
#     """
#     Tests the new_recipe view
#     """
#     def test_new_recipe_invalid_form(self):
#         """
#         Test the new_recipe view uses correct template when given invalid form
#         """

#         url = reverse('wordofmouth:new_recipe')
#         response = self.client.get(url, follow=True)

#         self.assertTemplateUsed(response, 'wordofmouth/recipe_experiment.html')