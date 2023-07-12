import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from sqlalchemy.orm import Session

from my_cookbook import models, schemas
from my_cookbook.api.v1.endpoints.recipes import read_recipes, create_recipe, delete_recipe, update_recipe


class TestRecipeBase(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)

    @property
    def returned_items(self):
        return [
            schemas.Recipe(
                name="batata", duration="1min", serves=2, owner_id=1, items=[]
            ),
            schemas.Recipe(
                name="batata2", duration="1min", serves=2, owner_id=1, items=[]
            ),
        ]


class TestGetRecipe(TestRecipeBase):
    @patch("my_cookbook.crud.recipe.get_multi")
    def test_list(self, mock_list):
        expected_response = self.returned_items
        mock_list.return_value = expected_response
        response = read_recipes(self.db)
        self.assertTrue(len(response) == len(expected_response))


class TestCreateRecipe(TestRecipeBase):
    def test_success(self):
        user_id = 1
        recipe_in = schemas.RecipeCreate(name="batata", duration="1min", serves=2)
        current_user = MagicMock(spec=models.User, id=user_id)
        response = create_recipe(recipe_in, self.db, current_user)
        self.assertTrue(response.name == recipe_in.name)


class TestUpdateRecipe(TestRecipeBase):
    @patch("my_cookbook.crud.recipe.get")
    def test_success_owner_id(self, recipe_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_mock.return_value = models.Recipe(
            id=1, name="batata", duration="1min", serves=2, owner_id=user_id
        )
        recipe_in = schemas.RecipeUpdate(name="batata2")
        response = update_recipe(
            db=self.db, id=1, recipe_in=recipe_in, current_user=current_user
        )
        self.assertTrue(response.name == recipe_in.name)

    @patch("my_cookbook.crud.recipe.get")
    def test_success_superuser(self, recipe_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=True)
        recipe_mock.return_value = models.Recipe(
            id=1, name="batata", duration="1min", serves=2, owner_id=user_id + 1
        )
        recipe_in = schemas.RecipeUpdate(name="batata2")
        response = update_recipe(
            db=self.db, id=1, recipe_in=recipe_in, current_user=current_user
        )
        self.assertTrue(response.name == recipe_in.name)

    @patch("my_cookbook.crud.recipe.get")
    def test_not_found(self, recipe_mock):
        recipe_mock.return_value = None
        with self.assertRaises(HTTPException):
            update_recipe(db=self.db, id=1, recipe_in=None, current_user=None)

    @patch("my_cookbook.crud.recipe.get")
    def test_permission_denied(self, recipe_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_mock.return_value = models.Recipe(
            id=1, name="batata", duration="1min", serves=2, owner_id=user_id + 1
        )
        recipe_in = schemas.RecipeUpdate(name="batata2")
        with self.assertRaises(HTTPException):
            update_recipe(
                db=self.db, id=1, recipe_in=recipe_in, current_user=current_user
            )


class TestDeleteRecipe(TestRecipeBase):
    @patch("my_cookbook.crud.recipe.get")
    def test_success_owner_id(self, recipe_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_mock.return_value = models.Recipe(
            id=1, name="batata", duration="1min", serves=2, owner_id=user_id
        )
        response = delete_recipe(db=self.db, id=1, current_user=current_user)
        self.assertTrue(response.name == recipe_mock.return_value.name)

    @patch("my_cookbook.crud.recipe.get")
    def test_success_superuser(self, recipe_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=True)
        recipe_mock.return_value = models.Recipe(
            id=1, name="batata", duration="1min", serves=2, owner_id=user_id + 1
        )
        response = delete_recipe(db=self.db, id=1, current_user=current_user)
        self.assertTrue(response.name == recipe_mock.return_value.name)

    @patch("my_cookbook.crud.recipe.get")
    def test_not_found(self, recipe_mock):
        recipe_mock.return_value = None
        with self.assertRaises(HTTPException):
            delete_recipe(db=self.db, id=1, current_user=None)

    @patch("my_cookbook.crud.recipe.get")
    def test_permission_denied(self, recipe_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_mock.return_value = models.Recipe(
            id=1, name="batata", duration="1min", serves=2, owner_id=user_id + 1
        )
        with self.assertRaises(HTTPException):
            delete_recipe(db=self.db, id=1, current_user=current_user)
