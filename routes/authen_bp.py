from flask import Blueprint,request, jsonify, session, make_response
from controller.AuthenticationController import AuthenticationController
import requests

authen_bp = Blueprint('authen_bp', __name__)
oauth_controller = AuthenticationController()

@authen_bp.route('/login', methods=['GET'])
def login():
    return oauth_controller.login()




