import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


#db_drop_and_create_all()

## ROUTES

@app.route('/drinks',methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    if not drinks:
        abort(404)

    formatted_drinks = [drink.short() for drink in drinks]
    return jsonify({
    "success": True,
    "drinks": formatted_drinks
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    drinks = Drink.query.all()
    if not drinks:
        abort(404)

    formatted_drinks = [drink.long() for drink in drinks]
    return jsonify({
    "success": True,
    "drinks": formatted_drinks
    })

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
    body = dict(request.get_json())
    if body is None:
        abort(400)

    title = body.get('title')
    recipe = body.get('recipe')
    try:
        if title and recipe:
            new_drink = Drink(title = title,
            recipe = json.dumps(recipe)
            )

            new_drink.insert()

            return jsonify({
            "success": True,
            "drinks": [new_drink.long()]
            })
        else:
            abort(422)
    except:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, drink_id):

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)

    body = dict(request.get_json())
    if body is None:
        abort(400)
    title = body.get('title')
    recipe = body.get('recipe')
    try:
        if title and recipe:
            drink.title = title
            drink.recipe = json.dumps(recipe)
            drink.update()

            return jsonify({
            "success": True,
            "drink": [drink.long()]
            })

        elif title and (recipe is None):
            drink.title = title
            drink.update()

            return jsonify({
            "success": True,
            "drink": [drink.long()]
            })
        elif recipe and (title is None):
            drink.recipe = json.dumps(recipe)
            drink.update()

            return jsonify({
            "success": True,
            "drink": [drink.long()]
            })
        else:
            abort(422)
    except:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
        "success": True,
        "delete": drink_id
        })
    except:
        abort(422)

## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(AuthError)
def AuthError(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "AuthError"
                    }), 401



@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": 'bad request'
                    }), 400
