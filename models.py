from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, Table, String, Boolean, Text, DateTime
from sqlalchemy import ARRAY
from sqlalchemy.orm import declarative_base, relationship
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from extensions import db

migrate = Migrate()


# Users Table Model
class Users(UserMixin, db.Model):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(100), nullable=False)
    likes = relationship("Likes", backref='user', cascade='all, delete')
    shoppingList = relationship("shoppingList", backref='shoppingList', cascade='all, delete')
    is_Admin = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    dateCreated = Column(DateTime, default=datetime.utcnow)
    
    def save_recipe(self, recipe):
        if not self.is_saved(recipe):
            like = Likes(user_id=self.id, recipe_id=recipe.id)
            db.session.add(like)
    
    def unsave_recipe(self, recipe):
        if self.is_saved(recipe):
            Likes.query.filter(
                Likes.recipe_id == recipe.id,
                Likes.user_id == self.id).delete()
            
    def is_saved(self, recipe):
        return Likes.query.filter(
            Likes.recipe_id == recipe.id,
            Likes.user_id == self.id).count() > 0
    
    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'likes': [recipe.format() for recipe in self.likes],
            'shoppingList': [item.format() for item in self.shoppingList],
            'is_Admin': self.is_Admin,
            'is_active': self.is_active,
            'dateCreated': self.dateCreated
        }

# Recipes Table Model
class Recipes(db.Model):
    __tablename__= "Recipes"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    imageURL = Column(String(300), nullable=True)
    videoURL = Column(String(300), nullable=True)
    category = Column(String(50), nullable=True)
    prepTime = Column(String(50), nullable=True)
    cookTime = Column(String(50), nullable=True)
    servings = Column(String(50), nullable=True)
    ingredients = relationship("Ingredients", backref='recipe', cascade='all, delete-orphan')
    reviews = relationship("Reviews", backref='recipe', cascade='all, delete-orphan')
    likes = relationship("Likes", backref='recipe', cascade='all, delete-orphan')
    ratingAvg = Column(String(10), nullable=True)
    ratingCount = Column(String(10), nullable=True)
    nutrition = relationship("Nutrition", backref='recipe', cascade='all, delete-orphan')
    dateCreated = Column(DateTime, default=datetime.utcnow)

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'ingredients': [ingredient.format() for ingredient in self.ingredients],
            'instructions': self.instructions,
            'imageURL': self.imageURL,
            'videoURL': self.videoURL,
            'category': self.category,
            'prepTime': self.prepTime,
            'cookTime': self.cookTime,
            'servings': self.servings,
            'reviews': [review.format() for review in self.reviews],
            'likes': [like.format() for like in self.likes],
            'ratingAvg': self.ratingAvg,
            'ratingCount': self.ratingCount,
            'nutrition': [nutrition.format() for nutrition in self.nutrition],
            'dateCreated': self.dateCreated
        }


# Ingredients Table Model
class Ingredients(db.Model):
    __tablename__= "Ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    unit = Column(String(50), nullable=True)
    amount = Column(String(100), nullable=True)
    recipe_id = Column(Integer, ForeignKey("Recipes.id"))
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'unit': self.unit,
            'amount': self.amount,
            'recipe_id': self.recipe_id
        }
    
    
class Nutrition(db.Model):
    __tablename__= "Nutrition"
    id = Column(Integer, primary_key=True)
    calories = Column(String(100), nullable=True)
    carbohydrate = Column(String(100), nullable=True)
    cholesterol = Column(String(100), nullable=True)
    fiber = Column(String(100), nullable=True)
    protein = Column(String(100), nullable=True)
    saturatedFat = Column(String(100), nullable=True)
    sodium = Column(String(100), nullable=True)
    sugar = Column(String(100), nullable=True)
    fat = Column(String(100), nullable=True)
    unsaturatedFat = Column(String(100), nullable=True)
    recipe_id = Column(Integer, ForeignKey("Recipes.id"))
    
    def format(self):
        return {
            'id': self.id,
            'calories': self.calories,
            'carbohydrate': self.carbohydrate,
            'cholesterol': self.cholesterol,
            'fiber': self.fiber,
            'protein': self.protein,
            'saturatedFat': self.saturatedFat,
            'sodium': self.sodium,
            'sugar': self.sugar,
            'fat': self.fat,
            'unsaturatedFat': self.unsaturatedFat,
            'recipe_id': self.recipe_id
        }
    
    
class Reviews(db.Model):
    __tablename__= "Reviews"
    id = Column(Integer, primary_key=True)
    author = Column(String(50), nullable=True)
    rating = Column(String(2), nullable=True)
    body = Column(String(300), nullable=True)
    recipe_id = Column(Integer, ForeignKey("Recipes.id"))
    
    def format(self):
        return {
            'id': self.id,
            'author': self.author,
            'rating': self.rating,
            'body': self.body,
            'recipe_id': self.recipe_id
        }
    
    
class shoppingList(db.Model):
    __tablename__ = "shoppingList"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    ingredient_id = Column(Integer)
    
    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'ingredient_id': self.ingredient_id
        }
    
    
# SavedRecipes Table Model
class Likes(db.Model):
    __tablename__= "Likes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    recipe_id = Column(Integer, ForeignKey("Recipes.id"))
    
    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recipe_id': self.recipe_id
        }