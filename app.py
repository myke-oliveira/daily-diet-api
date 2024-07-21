#! /usr/bin/env python

from flask import Flask, jsonify, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from bcrypt import hashpw, checkpw, gensalt
from database import db
from models.recipe import Recipe
from models.user import User

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
def create_recipe():
    pass

@app.route("/recipe/<int:recibe_id>", methods=["PUT"])
def update_recipe():
    pass

@app.route("/recipe/<int:recipe_id>", methods=["DELETE"])
def delete_recipe():
    pass

if __name__ == "__main__":
    app.run(debug=True)