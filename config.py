from flask import Flask, session
from flask_cors import CORS
import os
from dotenv import load_dotenv



def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key= os.urandom(24)

    CORS(app, resources={r'/*': {'origins': '*'}})
    MONGO_URI = os.environ.get('MONGO_URI')
    app.config["MONGO_URI"] = MONGO_URI
    from utils.extensions import timeloop

    timeloop.init_app(app)
    timeloop.start()
    return app

