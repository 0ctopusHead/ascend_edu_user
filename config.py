from flask import Flask, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_session import Session


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key= os.urandom(24)
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    Session(app)
    CORS(app, resources={r'/*': {'origins': '*'}})
    MONGO_URI = os.environ.get('MONGO_URI')
    app.config["MONGO_URI"] = MONGO_URI
    from utils.extensions import timeloop

    timeloop.init_app(app)
    timeloop.start()
    return app

