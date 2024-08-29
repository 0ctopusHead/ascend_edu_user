from flask import jsonify, request, redirect, session
from services.AuthenticationService import AuthenticationService

class AuthenticationController:
    def __init__(self):
        self.oauth_service = AuthenticationService()

    def login(self):
        login_url = self.oauth_service.get_login_url()
        return redirect(login_url)

    def handle_oauth_callback(self):
        code = request.args.get('code')
        if not code:
            return jsonify({'error': 'Authorization code not provided.'}), 400

        access_token = self.oauth_service.get_access_token(code)
        if not access_token:
            return jsonify({'error': 'Failed to obtain access token.'}), 400

        session['access_token'] = access_token
        print("Test: " + session['access_token'])
        user_info = self.oauth_service.get_user_info(access_token)
        print(user_info)
        if not user_info:
            return jsonify({'error': 'Failed to retrieve user information.'}), 400

        return jsonify({'message': 'Successfully logged in.'}), 200

    def user_info(self):
        try:
            access_token = session.get('access_token')
            user_info = self.oauth_service.get_user_info(access_token)
            if user_info:
                return user_info
            else:
                raise FileNotFoundError
        except Exception as e:
            return str(e), 401

    def get_stored_token(self):
        access_token = self.oauth_service.get_stored_token()
        return access_token

    def get_user_info(self, access_token):
        user_info = self.oauth_service.get_user_info(access_token)
        return user_info

    def get_access_token(self, code):
        access_token = self.oauth_service.get_access_token(code)
        return access_token