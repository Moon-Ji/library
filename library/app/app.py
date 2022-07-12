from flask import Flask
from flask_restx import Api, Resource
from main.controller.auth_controller import auth

from flask_migrate import Migrate
from db_connect import db
import config

def create_app():
    app = Flask(__name__)
    api = Api(app, title="Library's API Server")
    api.add_namespace(auth, '/auth')

    app.config.from_object(config)
    db.init_app(app)
    migrate = Migrate(app, db)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)