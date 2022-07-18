from flask_jwt_extended import create_access_token
import datetime

def create_token(email, user_id, token_type, iat):
    if token_type == 'access':
        expire_period = iat + datetime.timedelta(hours=1)
        payload = {}

    token = create_access_token(indentity=user_id)


