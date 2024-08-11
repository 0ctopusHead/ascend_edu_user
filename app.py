from flask_pymongo import PyMongo
from config import create_app
import os
app = create_app()
mongo = PyMongo(app)
db = mongo.db


if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)

    from routes.ask_bp import ask_bp
    app.register_blueprint(ask_bp)
    from routes.faqs_bp import faqs_bp
    app.register_blueprint(faqs_bp)

    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
