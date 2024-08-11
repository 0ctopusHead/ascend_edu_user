from flask_pymongo import PyMongo
from flask_cors import CORS
from config import create_app
import os

app = create_app()
CORS(app, resources={r'/*': {'origins': '*'}})
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)
db = mongo.db


def register_blueprints(app):
    from routes.ask_bp import ask_bp
    app.register_blueprint(ask_bp)

    from routes.faqs_bp import faqs_bp
    app.register_blueprint(faqs_bp)


register_blueprints(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
