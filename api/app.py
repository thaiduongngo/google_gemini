from flask import Flask
from api.routes import blueprint
from flask_cors import CORS


RESOURCES = {
    r"/api/*": {
        "origins": "*"
    }
}


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    CORS(
        app=app,
        resources=RESOURCES
    )
    return app
