from my_cookbook.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Recipe(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    duration = Column(String)
    serves = Column(Integer)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="recipes")
    items = relationship("RecipeItem", back_populates="recipe")


class RecipeItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    recipe = relationship("Recipe", back_populates="items")
    ingredients = relationship("Ingredient", back_populates="recipe_item")
    steps = relationship("Step", back_populates="recipe_item")


class Step(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    recipe_item_id = Column(Integer, ForeignKey("recipeitem.id"))
    recipe_item = relationship("RecipeItem", back_populates="steps")
    order = Column(Integer)
    description = Column(String)


class Ingredient(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(String)
    recipe_item_id = Column(Integer, ForeignKey("recipeitem.id"))
    recipe_item = relationship("RecipeItem", back_populates="ingredients")