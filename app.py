from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config["MONGO_URI"] = "mongodb://localhost:27017/ascend-edu"
mongo = PyMongo(app)
db = mongo.db

if __name__ == '__main__':
    from routes.ask_bp import ask_bp
    app.register_blueprint(ask_bp)

    app.run(debug=True, port=5001)
