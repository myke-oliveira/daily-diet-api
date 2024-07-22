#! /usr/bin/env python

from flask import Flask, jsonify, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from bcrypt import hashpw, checkpw, gensalt
from database import db
from models.recipe import Recipe
from models.user import User
from datetime import datetime

DATA_BASE_CONNECTION_STRING = "sqlite:///datababase.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secrete_key"
app.config["SQLALCHEMY_DATABASE_URI"] = DATA_BASE_CONNECTION_STRING

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "login"

@app.route("/user", methods=["POST"])
def create_user():
    username = request.json.get("username")
    password = request.json.get("password")
    
    if not username or not password:
        return jsonify({
            "message": "Invalid credentials"
        }), 400
        
    existent_user = User.query.filter_by(username=username).first()
    
    if existent_user:
        return jsonify({
            "message": "User alredy exist"
        }), 422
    
    hashed_password = hashpw(str.encode(password), gensalt())
    new_user = User(username=username, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "User created",
        "user": new_user.as_dict()
    }), 201
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    
    if not username or not password:
        return jsonify({"message": "Invalid credentials"}), 422
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not checkpw(password.encode(), user.password):
        return jsonify({"message": "Invalid credentials"}), 422
    
    login_user(user)
    
    return jsonify({"message": "User authenticated"})

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})

@app.route("/recipe", methods=["POST"])
@login_required
def create_recipe():
    name = request.json.get("name")
    description = request.json.get("description")
    date_time = request.json.get("date_time")
    on_the_diet = request.json.get("on_the_diet")
    
    if not name or not description or type(on_the_diet) != bool:
        return jsonify({"message": "Invalid Request"}), 400
    
    try:
        date_time = datetime.fromisoformat(date_time)
    except (TypeError, ValueError) as error:
        return jsonify({"message": "Invalid Request"}), 400
    
    recipe = Recipe(
        name=name,
        description=description,
        date_time=date_time,
        on_the_diet=on_the_diet,
        user_id=current_user.id,
        created_at=datetime.now(),
        last_modifiled_at=datetime.now()
    )
    
    db.session.add(recipe)
    db.session.commit()
    
    return jsonify({
        "message": "Recipe created",
        "recipe": recipe.as_dict()
    }), 201

@app.route("/recipe/<int:recipe_id>", methods=["PUT"])
@login_required
def update_recipe(recipe_id):
    name = request.json.get("name")
    description = request.json.get("description")
    date_time = request.json.get("date_time")
    on_the_diet = request.json.get("on_the_diet")
    
    if not name or not description or type(on_the_diet) != bool:
        return jsonify({"message": "Invalid Request"}), 400
    
    try:
        date_time = datetime.fromisoformat(date_time)
    except (TypeError, ValueError) as error:
        return jsonify({"message": "Invalid Request"}), 400
    
    recipe = Recipe.query.get(recipe_id)
    
    if not recipe or recipe.user_id != current_user.id:
        return jsonify({"message": "Recipe does not exist"}), 404
    
    recipe.name = name
    recipe.description = description
    recipe.date_time = date_time
    recipe.on_the_diet = on_the_diet
    recipe.last_modifiled = datetime.now()
    
    db.session.commit()
    
    return jsonify({
        "message": "Recipe updated",
        "recipe": recipe.as_dict()
    })

@app.route("/recipe/<int:recipe_id>", methods=["DELETE"])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    
    if not recipe or recipe.user_id != current_user.id:
        return jsonify({"message": "Recipe does not exist"}), 404
    
    db.session.delete(recipe)
    db.session.commit()
    
    return jsonify({"message": "Recipe deleted"})


@app.route("/recipe", methods=["GET"])
@login_required
def list_recipes():
    user_id = request.args.get("user_id")
    
    if user_id is None:
        recipes = Recipe.query.all()
    else:
        recipes = Recipe.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        "recipes": [recipe.as_dict() for recipe in recipes],
        "count": len(recipes)
    })

if __name__ == "__main__":
    app.run(debug=True)