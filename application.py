from flask import Flask, request, jsonify, make_response, abort
from flask_restful import Api
from config import Config
from models import *
from functools import wraps
from util import util
import datetime, jwt, json, random
from extensions import db, ma, migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

def register_extensions(application):
    db.app = application
    db.init_app(application)
    ma.app = application
    ma.init_app(application)
    CORS(application)
    migrate.init_app(application, db)

def register_resources(application):
    
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return jsonify({'message' : 'Token is missing!'}), 401

            try: 
                data = jwt.decode(token, application.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = Users.query.filter_by(id=data['id']).first()
                
            except:
                return jsonify({'message' : 'Token is invalid!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated

    @application.route('/users', methods=['GET'])
    @token_required
    def get_all_users(current_user):
        users = Users.query.all()
        if len(users) == 0:
            abort(404, 'No users found')
        return jsonify({
            'Users': [user.format() for user in users]
        })


    @application.route('/user/<id>', methods=['GET'])
    @token_required
    def get_one_user(current_user, id):
        user = Users.query.filter_by(id=id).first()
        print(id)
        if not user:
            return jsonify({'message' : 'No user found!', 'status': 0})
        return jsonify({'user' : user.format(), 'status': 200})
    
    @application.route('/user/favourites', methods=['GET'])
    @token_required
    def get_user_favourites(current_user):
        print(current_user.likes)
        likes = current_user.likes
        favourites = []
        for like in likes: 
            print(like.recipe_id)
        recipes = Recipes.query.filter(Recipes.id.in_(likes.recipe_id)).all()
        print(recipes)
        if not recipes:
            return jsonify({'recipes' : 'User has no likes!', 'status': 0})
        return jsonify({'recipes' : recipes.format(), 'status': 200})
    
    @application.route('/currentuser', methods=['GET'])
    @token_required
    def get_current_user(current_user):
        user = Users.query.filter_by(id=current_user.id).first()
        return jsonify({'user' : user.format(), 'status': 200})


    @application.route('/createuser', methods=['POST'])
    def create_user():
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = Users(username=data['username'], email=data['email'], password=hashed_password, is_Admin=False)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message' : 'New user created!', 'status': 200})


    @application.route('/promoteuser/<id>', methods=['PUT'])
    @token_required
    def promote_user(current_user, id):
        if not current_user.is_Admin:
            return jsonify({'message' : 'Cannot perform that function!', 'status': 100})
        user = Users.query.filter_by(id=id).first()
        if not user:
            return jsonify({'message' : 'No user found!', 'status': 0})
        user.is_Admin = True
        db.session.commit()
        return jsonify({'message' : 'The user has been promoted!', 'status': 200})

    @application.route('/demoteuser/<id>', methods=['PUT'])
    @token_required
    def demote_user(current_user, id):
        if not current_user.is_Admin:
            return jsonify({'message' : 'Cannot perform that function!', 'status': 100})
        user = Users.query.filter_by(id=id).first()
        if not user:
            return jsonify({'message' : 'No user found!', 'status': 0})
        user.is_Admin = False
        db.session.commit()
        return jsonify({'message' : 'The user has been demoted!', 'status': 200})

    @application.route('/user/<id>', methods=['DELETE'])
    @token_required
    def delete_user(current_user, id):
        if not current_user.is_Admin:
            return jsonify({'message' : 'Cannot perform that function!', 'status': 100})
        user = Users.query.filter_by(id=id).first()
        if not user:
            return jsonify({'message' : 'No user found!', 'status': 0})
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message' : 'The user has been deleted!', 'status': 200})


    @application.route('/login', methods=['POST'])
    def login():
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        user = Users.query.filter_by(username=auth.username).first()
        print(user)
        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1)}, Config.SECRET_KEY, algorithm="HS256")
            return jsonify({'token' : token})
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


    @application.route('/search', methods=['POST'])
    def searchByName():
        title = request.get_json()
        results = Recipes.query.filter(Recipes.title.like('%' + title['query'] + '%')).all()
        formated_results = []
        for result in results:
            formated_results.append(result.format())
        return jsonify({'results' : formated_results, 'status': 200})
    
    
    @application.route('/search/ingredients', methods=['GET'])
    def searchByIngredients():
        inputIngredients = request.get_json()['ingredients']
        results = Recipes.query.filter(Recipes.ingredients.any(Ingredients.name.in_(inputIngredients))).all()
        formated_results = []
        for result in results:
            formated_results.append(result.format())
        return jsonify({'results' : formated_results, 'status': 200})
        

    @application.route('/recipes', methods=['GET'])
    def get_all_recipes():
        recipes = Recipes.query.all()
        count = Recipes.query.count()
        if len(recipes) == 0:
            abort(404, 'No recipes found')
            
        randomRecipes = random.choices(recipes, k=50)
        return jsonify({'recipes' : [recipe.format() for recipe in randomRecipes], 'count' : count, 'status': 200})

    @application.route('/recipe/<id>', methods=['GET'])
    def get_one_recipe(id):
        recipe = Recipes.query.filter_by(id=id).first()
        if not recipe:
            return jsonify({'message' : 'No recipe found!', 'status': 0})
        return jsonify(recipe.format())


    @application.route('/recipe', methods=['POST'])
    @token_required
    def create_recipe(current_user):
        data = request.get_json()
        print(request.get_json())
        new_recipe = Recipes(data)
        print(new_recipe)
        # db.session.add(new_recipe)
        # db.session.commit()

        return jsonify({'message' : "recipe created!", 'status': 200})
    
    
    @application.route('/saverecipe/<int:recipe_id>', methods=['POST'])
    @token_required
    def save_recipe(current_user, recipe_id):
        recipe = Recipes.query.filter_by(id=recipe_id).first_or_404()
        current_user.save_recipe(recipe)
        db.session.commit()
        return jsonify({'message' : "Recipe added to favourites!", 'status': 200})
    
    @application.route('/unsaverecipe/<int:recipe_id>', methods=['POST'])
    @token_required
    def unsave_recipe(current_user, recipe_id):
        recipe = Recipes.query.filter_by(id=recipe_id).first_or_404()
        is_saved = current_user.is_saved(recipe)
        if(is_saved == False):
            return jsonify({'message' : "Recipe not in favourites!", 'status': 0})
        current_user.unsave_recipe(recipe)
        db.session.commit()
        return jsonify({'message' : "Recipe removed from favourites!", 'status': 200})
    
    @application.route('/issaved/<int:recipe_id>', methods=['POST'])
    @token_required
    def is_saved(current_user, recipe_id):
        recipe = Recipes.query.filter_by(id=recipe_id).first_or_404()
        return current_user.is_saved(recipe)


    @application.route('/recipe/<id>', methods=['PUT'])
    @token_required
    def edit_recipe(current_user, id):
        recipe = Recipes.query.filter_by(id=id).first()
        new_recipe = request.get_json()

        if not recipe:
            return jsonify({'message' : 'No recipe found!', 'status': 0})

        # recipe = new_recipe
        print(recipe)
        print(new_recipe)
        db.session.commit()

        return jsonify({'message' : 'recipe item has been edited!', 'status': 200})


    @application.route('/recipe/<id>', methods=['DELETE'])
    @token_required
    def delete_recipe(current_user, id):
        recipe = Recipes.query.filter_by(id=id).first()

        if not Recipes:
            return jsonify({'message' : 'No Recipe Found!', 'status': 0})

        db.session.delete(recipe)
        db.session.commit()

        return jsonify({'message' : 'Recipe Deleted!', 'status': 200})


    @application.route('/shoppinglist', methods=['GET'])
    @token_required
    def get_shopping_list(current_user):
        print(current_user)
        user = Users.query.filter_by(id=current_user.id).first()
        shoppinglist = user.shoppingList
        if len(shoppinglist) == 0:
            abort(404, 'No items found')
        return jsonify({
            'shoppingList': [item.format() for item in shoppinglist]
        })
        
    @application.route('/shoppinglist/<ids>', methods=['POST'])
    @token_required
    def add_to_shopping_list(current_user, ids):
        user = Users.query.filter_by(id=current_user.id).first()
        
        strippedString = ids.lstrip("[").rstrip("]")
        ingredients = strippedString.split(', ')
        
        def exists(ingredient):
            for shoppingList in user.shoppingList:
                if shoppingList.ingredient_id == ingredient.id:
                    return True
            return False
        
        for ingredientID in ingredients:
            ingredient = Ingredients.query.filter_by(id=ingredientID).one()
            if exists(ingredient):
                print('already exists')
            else:
                print('adding item')
                shoppingListItem = shoppingList(ingredient_id=ingredient.id)
                user.shoppingList.append(shoppingListItem)
            
        db.session.commit()
        return jsonify({'message' : 'Added to shopping list', 'status': 200})

    
    @application.route('/populate', methods=['POST'])
    def populate():
        util.populate()
        return jsonify({'message' : 'Populated Database!', 'status': 200})


application = Flask(__name__)
application.config.from_object(Config)

register_extensions(application)
register_resources(application)

if __name__ == '__main__':
    application.debug = True
    application.run()
    

