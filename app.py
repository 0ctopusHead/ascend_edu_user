from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery


app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})
app.config["MONGO_URI"] = "mongodb://localhost:27017/ascend-edu"
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

mongo = PyMongo(app)
db = mongo.db

celery = make_celery(app)

if __name__ == '__main__':
    from routes.ask_bp import ask_bp
    app.register_blueprint(ask_bp)
    from routes.faqs_bp import faqs_bp
    app.register_blueprint(faqs_bp)
    app.run(debug=True, port=5001)
