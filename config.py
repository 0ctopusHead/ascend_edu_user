from flask import Flask
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config["MONGO_URI"] = os.getenv("MONGO_IP_ADDRESS")

    from utils.extensions import timeloop
    timeloop.init_app(app)
    timeloop.start()
    return app
