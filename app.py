from flask import Flask, request, jsonify, make_response, abort
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from models import *
from functools import wraps
from util import util
import datetime, jwt
from extensions import db, ma
from werkzeug.security import generate_password_hash, check_password_hash



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.app = app
    db.init_app(app)
    ma.app = app
    ma.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app):
    
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                return jsonify({'message' : 'Token is missing!'}), 401

            try: 
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = Users.query.filter_by(id=data['id']).first()
                
            except:
                return jsonify({'message' : 'Token is invalid!'}), 401

            return f(current_user, *args, **kwargs)

        return decorated

    @app.route('/users', methods=['GET'])
    @token_required
    def get_all_users(current_user):
        users = Users.query.all()
        if len(users) == 0:
            abort(404, 'No users found')
        return jsonify({
            'Users': [user.format() for user in users]
        })


    @app.route('/user/<id>', methods=['GET'])
    @token_required
    def get_one_user(current_user, id):
        user = Users.query.filter_by(id=id).first()
        print(id)
        if not user:
            return jsonify({'message' : 'No user found!', 'status': 0})
        return jsonify({'user' : user.format(), 'status': 200})


    @app.route('/createuser', methods=['POST'])
    def create_user():
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = Users(username=data['username'], email=data['email'], password=hashed_password, is_Admin=False)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message' : 'New user created!', 'status': 200})


    @app.route('/promoteuser/<id>', methods=['PUT'])
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

    @app.route('/demoteuser/<id>', methods=['PUT'])
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

    @app.route('/user/<id>', methods=['DELETE'])
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


    @app.route('/login')
    def login():
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        user = Users.query.filter_by(username=auth.username).first()
        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1)}, Config.SECRET_KEY, algorithm="HS256")
            return jsonify({'token' : token})
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})



    @app.route('/recipes', methods=['GET'])
    def get_all_recipes():
        recipes = Recipes.query.all()
        count = Recipes.query.count()
        if len(recipes) == 0:
            abort(404, 'No recipes found')
        return jsonify({'recipes' : [recipe.format() for recipe in recipes], 'count' : count})

    @app.route('/recipe/<id>', methods=['GET'])
    def get_one_recipe(id):
        recipe = Recipes.query.filter_by(id=id).first()
        if not recipe:
            return jsonify({'message' : 'No recipe found!', 'status': 0})
        return jsonify(recipe.format())


    @app.route('/recipe', methods=['POST'])
    @token_required
    def create_recipe(current_user):
        data = request.get_json()
        print(request.get_json())
        new_recipe = Recipes(data)
        print(new_recipe)
        # db.session.add(new_recipe)
        # db.session.commit()

        return jsonify({'message' : "recipe created!", 'status': 200})

    @app.route('/recipe/<id>', methods=['PUT'])
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


    @app.route('/recipe/<id>', methods=['DELETE'])
    @token_required
    def delete_recipe(current_user, id):
        recipe = Recipes.query.filter_by(id=id).first()

        if not Recipes:
            return jsonify({'message' : 'No Recipe Found!', 'status': 0})

        db.session.delete(recipe)
        db.session.commit()

        return jsonify({'message' : 'Recipe Deleted!', 'status': 200})


    @app.route('/shoppinglist', methods=['GET'])
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
        
    @app.route('/shoppinglist/<ids>', methods=['POST'])
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

    
    @app.route('/populate', methods=['POST'])
    def populate():
        util.populate()
        return jsonify({'message' : 'Populated Database!', 'status': 200})




if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=4000)
    

