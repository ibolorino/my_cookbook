import unittest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from my_cookbook import models, schemas
from my_cookbook.api.v1.endpoints.step import (
    read_steps,
    create_step,
    update_step,
    delete_step,
)


class TestStepBase(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
    
    @property
    def returned_items(self):
        return [
            schemas.Step(name="batata", order=1, description="batata", recipe_item_id=1),
            schemas.Step(name="batata", order=2, description="batata", recipe_item_id=1),
        ]
    

class TestGetStep(TestStepBase):
    @patch("my_cookbook.crud.step.get_multi")
    def test_list(self, steps_mock):
        steps_mock.return_value = self.returned_items
        response = read_steps(self.db)
        self.assertTrue(len(response) == len(self.returned_items))


class TestCreateStep(TestStepBase):
    @patch("my_cookbook.crud.recipe_item.get")
    def test_success_owner_id(self, recipe_item_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        step_in = schemas.StepCreate(name="batata", order=1, description="batata", recipe_item_id=1)
        recipe_item_mock.return_value = models.RecipeItem(id=1, name="batata", steps=[], ingredients=[], recipe=MagicMock(owner_id=user_id))
        response = create_step(step_in, self.db, current_user)
        self.assertTrue(response.name == step_in.name)
    
    @patch("my_cookbook.crud.recipe_item.get")
    def test_permission_denied(self, recipe_item_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        step_in = schemas.StepCreate(name="batata", order=1, description="batata", recipe_item_id=1)
        recipe_item_mock.return_value = models.RecipeItem(id=1, name="batata", steps=[], ingredients=[], recipe=MagicMock(owner_id=user_id+1))
        with self.assertRaises(HTTPException):
            create_step(step_in, self.db, current_user)


class TestUpdateStep(TestStepBase):
    @patch("my_cookbook.crud.step.get")
    def test_success_owner_id(self, step_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        step_in = schemas.StepCreate(name="batata2", order=1, description="batata", recipe_item_id=1)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id))
        step_mock.return_value = models.Step(id=1, name="batata", order=1, description="batata", recipe_item=recipe_item)
        response = update_step(db=self.db, id=1, step_in=step_in, current_user=current_user)
        self.assertTrue(response.name == step_in.name)

    @patch("my_cookbook.crud.step.get")
    def test_success_superuser(self, step_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=True)
        step_in = schemas.StepCreate(name="batata2", order=1, description="batata", recipe_item_id=1)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id+1))
        step_mock.return_value = models.Step(id=1, name="batata", order=1, description="batata", recipe_item=recipe_item)
        response = update_step(db=self.db, id=1, step_in=step_in, current_user=current_user)
        self.assertTrue(response.name == step_in.name)

    @patch("my_cookbook.crud.step.get")
    def test_not_found(self, step_mock):
        step_mock.return_value = None
        with self.assertRaises(HTTPException):
            update_step(db=self.db, id=1, step_in=None, current_user=None)

    
    @patch("my_cookbook.crud.step.get")
    def test_permission_denied(self, step_mock):
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        step_in = schemas.StepCreate(name="batata2", order=1, description="batata", recipe_item_id=1)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id+1))
        step_mock.return_value = models.Step(id=1, name="batata", order=1, description="batata", recipe_item=recipe_item)
        with self.assertRaises(HTTPException):
            update_step(db=self.db, id=1, step_in=step_in, current_user=current_user)


class TestDeleteStep(TestStepBase):
    @patch("my_cookbook.crud.step.get")
    def test_success_owner_id(self, step_mock):
        step_id = 1
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id))
        step_mock.return_value = models.Step(id=1, name="batata", order=1, description="batata", recipe_item=recipe_item)
        response = delete_step(db=self.db, id=step_id, current_user=current_user)
        self.assertTrue(response.name == step_mock.return_value.name)
    
    @patch("my_cookbook.crud.step.get")
    def test_success_superuser(self, step_mock):
        step_id = 1
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=True)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id+1))
        step_mock.return_value = models.Step(id=1, name="batata", order=1, description="batata", recipe_item=recipe_item)
        response = delete_step(db=self.db, id=step_id, current_user=current_user)
        self.assertTrue(response.name == step_mock.return_value.name)
    
    @patch("my_cookbook.crud.step.get")
    def test_not_found(self, step_mock):
        step_mock.return_value = None
        with self.assertRaises(HTTPException):
            delete_step(db=self.db, id=1, current_user=None)

    @patch("my_cookbook.crud.step.get")
    def test_permission_denied(self, step_mock):
        step_id = 1
        user_id = 1
        current_user = MagicMock(spec=models.User, id=user_id, is_superuser=False)
        recipe_item = MagicMock(recipe=MagicMock(owner_id=user_id+1))
        step_mock.return_value = models.Step(id=1, name="batata", order=1, description="batata", recipe_item=recipe_item)
        with self.assertRaises(HTTPException):
            delete_step(db=self.db, id=step_id, current_user=current_user)
