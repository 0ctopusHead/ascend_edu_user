from flask import Flask


def create_app():
    app = Flask(__name__)
    from utils.extensions import timeloop
    timeloop.init_app(app)
    timeloop.start()
    return app
