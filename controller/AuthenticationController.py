from flask import redirect, url_for, session, request, jsonify
from services.AuthenticationService import AuthenticationService

class CMUOAuthController:
    def __init__(self, oauth_service):
        self.oauth_service = oauth_service

    def login(self):
        authorization_url = self.oauth_service.get_authorization_url()
        return redirect(authorization_url)

    def callback(self):
        try:
            token = self.oauth_service.fetch_token(request.url)
            user_info = self.oauth_service.get_user_info(token)

            if self.oauth_service.is_cmu_student(user_info):
                session['user'] = user_info
                return redirect(url_for('ask_bp.authenticated'))
            else:
                return jsonify({'error': 'User is not a CMU student'}), 401

        except Exception as e:
            return jsonify({'error': str(e)}), 500
