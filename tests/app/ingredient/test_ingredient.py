import unittest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from my_cookbook import models, schemas
from my_cookbook.api.v1.endpoints.ingredient import (
    read_ingredients,
    create_ingredient,
    update_ingredient,
    delete_ingredient,
)


class TestIngredientBase(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
    
    @property
    def returned_items(self):
        return [
            schemas.Ingredient(name="batata", quantity="500g", recipe_item_id=1),
            schemas.Ingredient(name="batata2", quantity="500g", recipe_item_id=1),
        ]
    

class TestGetIngredient(TestIngredientBase):
    @patch("my_cookbook.crud.ingredient.get_multi")
    def test_list(self, ingredients_mock):
        expected_response = self.returned_items
        ingredients_mock.return_value = expected_response
        response = read_ingredients(self.db)
        self.assertTrue(len(response) == len(expected_response))


class TestCreateIngredient(TestIngredientBase):
    @patch("my_cookbook.crud.recipe_item.get")
    def test_success_owner_id(self, recipe_item_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        ingredient_in = schemas.IngredientCreate(name="batata", quantity="500g", recipe_item_id=1)
        recipe_item_mock.return_value = models.RecipeItem(id=1, name="batata", steps=[], ingredients=[], recipe=MagicMock(owner_id=user_id))
        response = create_ingredient(ingredient_in, self.db, current_user)
        self.assertTrue(response.name == ingredient_in.name)
    
    @patch("my_cookbook.crud.recipe_item.get")
    def test_success_permission_denied(self, recipe_item_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        ingredient_in = schemas.IngredientCreate(name="batata", quantity="500g", recipe_item_id=1)
        recipe_item_mock.return_value = models.RecipeItem(id=1, name="batata", steps=[], ingredients=[], recipe=MagicMock(owner_id=user_id+1))
        with self.assertRaises(HTTPException):
            create_ingredient(ingredient_in, self.db, current_user)


class TestUpdateIngredient(TestIngredientBase):
    @patch("my_cookbook.crud.ingredient.get")
    def test_success_owner_id(self, ingredient_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        ingredient_in = schemas.IngredientCreate(name="batata", quantity="500g", recipe_item_id=1)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id))
        ingredient_mock.return_value = models.Ingredient(id=1, name="batata", quantity="500g", recipe_item=recipe_item)
        response = update_ingredient(db=self.db, id=1, ingredient_in=ingredient_in, current_user=current_user)
        self.assertTrue(response.name == ingredient_in.name)

    @patch("my_cookbook.crud.ingredient.get")
    def test_success_superuser(self, ingredient_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=True)
        ingredient_in = schemas.IngredientCreate(name="batata", quantity="500g", recipe_item_id=1)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id+1))
        ingredient_mock.return_value = models.Ingredient(id=1, name="batata", quantity="500g", recipe_item=recipe_item)
        response = update_ingredient(db=self.db, id=1, ingredient_in=ingredient_in, current_user=current_user)
        self.assertTrue(response.name == ingredient_in.name)

    @patch("my_cookbook.crud.ingredient.get")
    def test_not_found(self, ingredient_mock):
        ingredient_mock.return_value = None
        with self.assertRaises(HTTPException):
            update_ingredient(db=self.db, id=1, ingredient_in=None, current_user=None)

    @patch("my_cookbook.crud.ingredient.get")
    def test_premission_denied(self, ingredient_mock):    
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        ingredient_in = schemas.IngredientCreate(name="batata", quantity="500g", recipe_item_id=1)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id+1))
        ingredient_mock.return_value = models.Ingredient(id=1, name="batata", quantity="500g", recipe_item=recipe_item)
        with self.assertRaises(HTTPException):
            update_ingredient(db=self.db, id=1, ingredient_in=ingredient_in, current_user=current_user)


class TestDeleteIngredient(TestIngredientBase):
    @patch("my_cookbook.crud.ingredient.get")
    def test_success_owner_id(self, ingredient_mock):
        ingredient_id = 1
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id))
        ingredient_mock.return_value = models.Ingredient(id=1, name="batata", quantity="500g", recipe_item=recipe_item)
        response = delete_ingredient(db=self.db, id=ingredient_id, current_user=current_user)
        self.assertTrue(response.name == ingredient_mock.return_value.name)
    
    @patch("my_cookbook.crud.ingredient.get")
    def test_success_owner_id(self, ingredient_mock):
        ingredient_id = 1
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id))
        ingredient_mock.return_value = models.Ingredient(id=1, name="batata", quantity="500g", recipe_item=recipe_item)
        response = delete_ingredient(db=self.db, id=ingredient_id, current_user=current_user)
        self.assertTrue(response.name == ingredient_mock.return_value.name)

    @patch("my_cookbook.crud.ingredient.get")
    def test_not_found(self, ingredient_mock):
        ingredient_mock.return_value = None
        with self.assertRaises(HTTPException):
            delete_ingredient(db=self.db, id=1, current_user=None)
    
    @patch("my_cookbook.crud.ingredient.get")
    def test_permission_denied(self, ingredient_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id+1))
        ingredient_mock.return_value = models.Ingredient(id=1, name="batata", quantity="500g", recipe_item=recipe_item)
        with self.assertRaises(HTTPException):
            delete_ingredient(db=self.db, id=1, current_user=current_user)
