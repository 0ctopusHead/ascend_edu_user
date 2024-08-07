from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config["MONGO_URI"] = "mongodb://localhost:27017/ascend-edu"
    from utils.extensions import timeloop
    timeloop.init_app(app)
    timeloop.start()
    return app
