import datetime
from flask import request, make_response, abort
from bcrypt import hashpw, checkpw, gensalt
from flask_jwt_extended import create_access_token, create_refresh_token

from db_connect import db
from common.regex import validate_email, validate_password
from models.user import User

# 회원가입
def register_user(request_body):
    email = request_body['email']
    password1 = request_body['password1']
    password2 = request_body['password2']
    name = request_body['name']

    # 유효성 검사
    if email == None or password1 == None or password2 == None or name == None:
        abort(400, 'Register Fail')

    if email == '' or password1 == '' or password2 == '' or name == '':
        abort(400, 'Register Fail')

    if not validate_email(email):
        abort(400, 'Invalid Email')

    if not validate_password(password1):
        abort(400, 'Invalid Password')

    if not password1 == password2:
        abort(400, 'Password Not Same')

    check_user = User.query.filter(User.email == email).first()

    if check_user:
        abort(400, "Already exist")
    
    # 신규 유저 생성
    pw_hash = hashpw(password1.encode("utf-8"), gensalt())
    
    new_user = User(
        email=email,
        password=pw_hash,
        name=name
    )
    
    db.session.add(new_user)
    db.session.commit()

    return "Register success"

def login_user(request_body):
    email = request_body['email']
    password = request_body['password']

    user = User.query.filter(User.email == email).first()
    if not user:
        abort(400, "User Not Found")

    pw_check = checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
    if not pw_check:
        abort(400, "Wrong Password")

    user_id = user.id
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    if not update_user_refresh_token(user_id, refresh_token):
        abort(400, 'Fail To Generate Token')

    response_data = {
        'token':access_token,
        'message': 'login suceess'
    }

    return response_data

def update_user_refresh_token(user_id, refresh_token):
    target_user = User.query.filter(User.id == user_id).first()
    try:
        target_user.refresh_token = refresh_token
        db.session.commit()
    except:
        return False
    else:
        return True