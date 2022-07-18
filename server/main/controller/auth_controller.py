from flask import request, jsonify
from flask_restx import Resource, Api, Namespace, fields

from service.user_service import register_user, login_user

auth = Namespace(name='Auth', description="사용자 인증을 위한 API")

user_model = auth.model("user", {
    "email": fields.String(description="user email")
})

@auth.route('/register')
class Register(Resource):
    @auth.response(200, "회원가입을 성공했습니다.")
    @auth.response(400, "Failed")
    def post(self):
        """회원가입을 진행합니다."""
        request_body = request.get_json()
        return register_user(request_body), 200

@auth.route('/login')
class Login(Resource):
    def post(self):
        """로그인을 진행합니다."""
        request_body = request.get_json()
        return login_user(request_body), 200