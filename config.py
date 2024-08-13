from flask import Flask
from flask_cors import CORS
import os


def create_app():

    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    MONGO_URI = os.environ.get('MONGO_URI')
    app.config["MONGO_URI"] = MONGO_URI
    from utils.extensions import timeloop

    timeloop.init_app(app)
    timeloop.start()
    return app

