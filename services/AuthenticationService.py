# from requests_oauthlib import OAuth2Session
# from flask import session
from flask import request, jsonify, session
import os
from dotenv import load_dotenv
import requests

load_dotenv()
REDIRECT_URI = 'https://lineedu.ascendedu.systems/login_callback'
AUTH_ENDPOINT = 'https://oauth.cmu.ac.th/v1/Authorize.aspx'
TOKEN_ENDPOINT = 'https://oauth.cmu.ac.th/v1/GetToken.aspx'
USERINFO_ENDPOINT = 'https://misapi.cmu.ac.th/cmuitaccount/v1/api/cmuitaccount/basicinfo'
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
CLIENT_ID = "C9VKwSmXsTJUYgheHucA0MwUQnz7QPu0XMKYy04H"

class AuthenticationService:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.redirect_uri = REDIRECT_URI
        self.access_token = None

    def get_login_url(self):
        login_url = f'{AUTH_ENDPOINT}?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=cmuitaccount.basicinfo'
        return login_url

    def get_access_token(self, code):
        data = {
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
        }

        response = requests.post(TOKEN_ENDPOINT, data=data)
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens.get('access_token')
            session['access_token'] = self.access_token
            return self.access_token
        else:
            return None

    def get_user_info(self, access_token):
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json',
            }
            response = requests.get(USERINFO_ENDPOINT, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise FileNotFoundError
        except Exception as e:
            raise e

    def get_stored_token(self):
        return self.access_token