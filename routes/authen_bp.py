from flask import Blueprint,request, jsonify, session, make_response
from controller.AuthenticationController import AuthenticationController
import requests

authen_bp = Blueprint('authen_bp', __name__)
oauth_controller = AuthenticationController()

@authen_bp.route('/login', methods=['GET'])
def login():
    return oauth_controller.login()


@authen_bp.route('/userinfo', methods=['GET'])
def user_info():
    return oauth_controller.user_info()


@authen_bp.route('/store_token', methods=['POST'])
def store_token():
    data = request.get_json()
    code = data.get('code')

    if code:
        access_token = oauth_controller.get_access_token(code)
        if access_token:
            return jsonify({'status': 'Token stored successfully', 'access_token': access_token}), 200
        else:
            return jsonify({'status': 'Failed to store token'}), 400
    return jsonify({'status': 'No code provided'}), 400


@authen_bp.route('/get_token', methods=['GET'])
def get_token():
    token = oauth_controller.get_stored_token()
    if token:
        return jsonify({'access_token': token}), 200
    return jsonify({'status': 'No token available'}), 404