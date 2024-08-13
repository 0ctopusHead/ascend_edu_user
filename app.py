from flask_pymongo import PyMongo
from config import create_app
from linebot import LineBotApi, WebhookHandler
import os

app = create_app()

mongo = PyMongo(app)
db = mongo.db

chanel_secret = os.environ.get('CHANEL_SECRET')
chanel_access_token = os.environ.get('CHANEL_ACCESS_TOKEN')

line_bot_api = LineBotApi(chanel_access_token)
handler = WebhookHandler(chanel_secret)


def register_blueprints(app):
    from routes.ask_bp import ask_bp
    app.register_blueprint(ask_bp)

    from routes.faqs_bp import faqs_bp
    app.register_blueprint(faqs_bp)


register_blueprints(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
