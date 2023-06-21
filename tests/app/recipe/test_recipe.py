import unittest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from my_cookbook import models, schemas, crud, create_app
from my_cookbook.api.v1.endpoints.recipe_items import (
    create_recipe_item, 
    update_recipe_item,
    delete_recipe_item,
)


class TestRecipeItemBase(unittest.TestCase):
    def setUp(self):
        pass

    @property
    def returned_items(self):
        return [
            {"name": "batata", "steps": [], "ingredients": []},
            {"name": "batata2", "steps": [], "ingredients": []}
        ]


class TestGetRecipeItem(TestRecipeItemBase):
    @patch("my_cookbook.crud.recipe_item.get_multi")
    def test_list(self, mock_list):
        app = create_app()
        client = TestClient(app)
        expected_response = self.returned_items
        mock_list.return_value = expected_response
        response = client.get("/api/v1/recipe_item")
        assert len(response.json()) == len(expected_response)
        

class TestCreateRecipeItem(TestRecipeItemBase): 
    def test_success(self):
        user_id = 1
        mock_db = MagicMock(spec=Session)
        recipe_item_in = schemas.RecipeItemCreate(recipe_id=1, name="batata")
        current_user = MagicMock(spec=models.User, id=user_id)
        crud.recipe.get = MagicMock(return_value=MagicMock(owner_id=user_id))
        response = create_recipe_item(recipe_item_in, mock_db, current_user)
        self.assertTrue(response.name == recipe_item_in.name)

    def test_permission_denied(self):
        user_id = 1
        mock_db = MagicMock(spec=Session)
        recipe_item_in = schemas.RecipeItemCreate(recipe_id=1, name="batata")
        current_user = MagicMock(spec=models.User, id=user_id+1)
        crud.recipe.get = MagicMock(return_value=MagicMock(owner_id=user_id))
        with self.assertRaises(HTTPException) as context:
            response = create_recipe_item(recipe_item_in, mock_db, current_user)


class TestUpdateRecipeItem(TestRecipeItemBase):
    @patch("my_cookbook.crud.recipe_item.get")
    def test_success_same_owner_id(self, recipe_item_mock):
        mock_db = MagicMock(spec=Session)
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_item_in = schemas.RecipeItemUpdate(name="nova batata")
        recipe_item_mock.return_value = models.RecipeItem(id=1, name="batata", steps=[], ingredients=[], recipe=MagicMock(owner_id=user_id))
        response = update_recipe_item(db=mock_db, id=user_id, recipe_item_in=recipe_item_in, current_user=current_user)
        assert(response.name == recipe_item_in.name)

    @patch("my_cookbook.crud.recipe_item.get")
    def test_success_superuser(self, recipe_item_mock):
        mock_db = MagicMock(spec=Session)
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=True)
        recipe_item_in = schemas.RecipeItemUpdate(name="nova batata")
        recipe_item_mock.return_value = models.RecipeItem(id=1, name="batata", steps=[], ingredients=[], recipe=MagicMock(owner_id=user_id+1))
        response = update_recipe_item(db=mock_db, id=user_id, recipe_item_in=recipe_item_in, current_user=current_user)
        assert(response.name == recipe_item_in.name)

    @patch("my_cookbook.crud.recipe_item.get")
    def test_not_found(self, recipe_item_mock):
        recipe_item_mock.return_value = None
        with self.assertRaises(HTTPException):
            update_recipe_item(db=None, id=1, recipe_item_in=None, current_user=None)

    @patch("my_cookbook.crud.recipe_item.get")
    def test_permission_denied(self, recipe_item_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        mock_db = MagicMock(spec=Session)
        recipe_item_in = schemas.RecipeItemUpdate(name="nova batata")
        recipe_item_mock.return_value = models.RecipeItem(id=1, name="batata2222", steps=[], ingredients=[], recipe=MagicMock(owner_id=user_id+1))
        with self.assertRaises(HTTPException):
            update_recipe_item(db=mock_db, id=1, recipe_item_in=recipe_item_in, current_user=current_user)


class TestDeleteRecipeItem(TestRecipeItemBase):
    @patch("my_cookbook.crud.recipe_item.get")
    def test_success_same_owner_id(self, recipe_item_mock):
        user_id = 1
        recipe_item_id = 1
        mock_db = MagicMock(spec=Session)
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_item_mock.return_value = models.RecipeItem(id=recipe_item_id, name="batata", steps=[], ingredients=[], recipe=MagicMock(owner_id=user_id))
        response = delete_recipe_item(db=mock_db, id=1, current_user=current_user)
        self.assertTrue(response.name == recipe_item_mock.return_value.name)

    @patch("my_cookbook.crud.recipe_item.get")
    def test_success_superuser(self, recipe_item_mock):
        user_id = 1
        recipe_item_id = 1
        mock_db = MagicMock(spec=Session)
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=True)
        recipe_item_mock.return_value = models.RecipeItem(id=recipe_item_id, name="batata", steps=[], ingredients=[], recipe=MagicMock(owner_id=user_id+1))
        response = delete_recipe_item(db=mock_db, id=1, current_user=current_user)
        self.assertTrue(response.name == recipe_item_mock.return_value.name)

    @patch("my_cookbook.crud.recipe_item.get")
    def test_not_found(self, recipe_item_mock):
        recipe_item_mock.return_value = None
        with self.assertRaises(HTTPException):
            delete_recipe_item(db=None, id=1, current_user=None)

    @patch("my_cookbook.crud.recipe_item.get")
    def test_permission_denied(self, recipe_item_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_item_mock.return_value = models.RecipeItem(id=1, name="batata2222", steps=[], ingredients=[], recipe=MagicMock(owner_id=user_id+1))
        with self.assertRaises(HTTPException):
            delete_recipe_item(db=None, id=1, current_user=current_user)
