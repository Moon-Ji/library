from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
from main.models.user import User

auth = Namespace('Auth')

@auth.route('')
class TestPost(Resource):
    def get(selt):
        user1 = User.query.filter_by(email="test").first()
        print(user1.id)
        return "test"