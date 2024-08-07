from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_timeloop import Timeloop
from config import create_app
from datetime import timedelta

app = create_app()
mongo = PyMongo(app)
db = mongo.db


if __name__ == '__main__':
    from routes.ask_bp import ask_bp
    app.register_blueprint(ask_bp)
    from routes.faqs_bp import faqs_bp
    app.register_blueprint(faqs_bp)

    app.run(debug=True, port=5001)
