import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from sqlalchemy.orm import Session

from my_cookbook import crud, models, schemas
from my_cookbook.api.v1.endpoints.recipe_items import (
    create_recipe_item,
    delete_recipe_item,
    read_recipe_items,
    update_recipe_item,
    update_recipe_item_steps
)


class TestRecipeItemBase(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)

    @property
    def returned_items(self):
        return [
            schemas.RecipeItem(name="batata", steps=[], ingredients=[]),
            schemas.RecipeItem(name="batata2", steps=[], ingredients=[]),
        ]


class TestGetRecipeItem(TestRecipeItemBase):
    @patch("my_cookbook.crud.recipe_item.get_multi")
    def test_list(self, mock_list):
        expected_response = self.returned_items
        mock_list.return_value = expected_response
        response = read_recipe_items(self.db)
        self.assertTrue(len(response) == len(expected_response))


class TestCreateRecipeItem(TestRecipeItemBase):
    def test_success(self):
        user_id = 1
        recipe_item_in = schemas.RecipeItemCreate(recipe_id=1, name="batata")
        current_user = MagicMock(spec=models.User, id=user_id)
        crud.recipe.get = MagicMock(return_value=MagicMock(owner_id=user_id))
        response = create_recipe_item(recipe_item_in, self.db, current_user)
        self.assertTrue(response.name == recipe_item_in.name)

    def test_permission_denied(self):
        user_id = 1
        recipe_item_in = schemas.RecipeItemCreate(recipe_id=1, name="batata")
        current_user = MagicMock(spec=models.User, id=user_id + 1)
        crud.recipe.get = MagicMock(return_value=MagicMock(owner_id=user_id))
        with self.assertRaises(HTTPException):
            create_recipe_item(recipe_item_in, self.db, current_user)


class TestUpdateRecipeItem(TestRecipeItemBase):
    @patch("my_cookbook.crud.recipe_item.get")
    def test_success_same_owner_id(self, recipe_item_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_item_in = schemas.RecipeItemUpdate(name="nova batata")
        recipe_item_mock.return_value = models.RecipeItem(
            id=1,
            name="batata",
            steps=[],
            ingredients=[],
            recipe=MagicMock(owner_id=user_id),
        )
        response = update_recipe_item(
            db=self.db,
            id=user_id,
            recipe_item_in=recipe_item_in,
            current_user=current_user,
        )
        self.assertTrue(response.name == recipe_item_in.name)

    @patch("my_cookbook.crud.recipe_item.get")
    def test_success_superuser(self, recipe_item_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=True)
        recipe_item_in = schemas.RecipeItemUpdate(name="nova batata")
        recipe_item_mock.return_value = models.RecipeItem(
            id=1,
            name="batata",
            steps=[],
            ingredients=[],
            recipe=MagicMock(owner_id=user_id + 1),
        )
        response = update_recipe_item(
            db=self.db,
            id=user_id,
            recipe_item_in=recipe_item_in,
            current_user=current_user,
        )
        assert response.name == recipe_item_in.name

    @patch("my_cookbook.crud.recipe_item.get")
    def test_not_found(self, recipe_item_mock):
        recipe_item_mock.return_value = None
        with self.assertRaises(HTTPException):
            update_recipe_item(db=None, id=1, recipe_item_in=None, current_user=None)

    @patch("my_cookbook.crud.recipe_item.get")
    def test_permission_denied(self, recipe_item_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_item_in = schemas.RecipeItemUpdate(name="nova batata")
        recipe_item_mock.return_value = models.RecipeItem(
            id=1,
            name="batata2222",
            steps=[],
            ingredients=[],
            recipe=MagicMock(owner_id=user_id + 1),
        )
        with self.assertRaises(HTTPException):
            update_recipe_item(
                db=self.db,
                id=1,
                recipe_item_in=recipe_item_in,
                current_user=current_user,
            )


class TestUpdateRecipeItemSteps(TestRecipeItemBase):
    @patch("my_cookbook.crud.recipe_item.get")
    def test_success(self, recipe_item_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        steps = [
            models.Step(name="batata", description="batata", id=1, order=1),
            models.Step(name="batata2", description="batata2", id=2, order=2),
        ]
        steps_in = [
            schemas.StepOrderUpdate(id=1, order=3),
            schemas.StepOrderUpdate(id=5, order=5),
        ]
        recipe_item_mock.return_value = models.RecipeItem(
            id=1,
            name="batata",
            steps=steps,
            ingredients=[],
            recipe=MagicMock(owner_id=user_id),
        )
        response = update_recipe_item_steps(
            db=self.db, id=1, steps_in=steps_in, current_user=current_user
        )
        for i, step in enumerate(recipe_item_mock.steps):
            self.assertTrue(step.order != response.steps[i].order)


class TestDeleteRecipeItem(TestRecipeItemBase):
    @patch("my_cookbook.crud.recipe_item.get")
    def test_success_same_owner_id(self, recipe_item_mock):
        user_id = 1
        recipe_item_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_item_mock.return_value = models.RecipeItem(
            id=recipe_item_id,
            name="batata",
            steps=[],
            ingredients=[],
            recipe=MagicMock(owner_id=user_id),
        )
        response = delete_recipe_item(db=self.db, id=1, current_user=current_user)
        self.assertTrue(response.name == recipe_item_mock.return_value.name)

    @patch("my_cookbook.crud.recipe_item.get")
    def test_success_superuser(self, recipe_item_mock):
        user_id = 1
        recipe_item_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=True)
        recipe_item_mock.return_value = models.RecipeItem(
            id=recipe_item_id,
            name="batata",
            steps=[],
            ingredients=[],
            recipe=MagicMock(owner_id=user_id + 1),
        )
        response = delete_recipe_item(db=self.db, id=1, current_user=current_user)
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
        recipe_item_mock.return_value = models.RecipeItem(
            id=1,
            name="batata2222",
            steps=[],
            ingredients=[],
            recipe=MagicMock(owner_id=user_id + 1),
        )
        with self.assertRaises(HTTPException):
            delete_recipe_item(db=None, id=1, current_user=current_user)
