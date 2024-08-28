from requests_oauthlib import OAuth2Session
from flask import session

class AuthenticationService:
    def __init__(self, client_id, client_secret, authorization_base_url, token_url, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_base_url = authorization_base_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri

    def get_authorization_url(self):
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri)
        authorization_url, state = oauth.authorization_url(self.authorization_base_url)
        session['oauth_state'] = state
        return authorization_url

    def fetch_token(self, authorization_response):
        oauth = OAuth2Session(self.client_id, state=session.get('oauth_state'), redirect_uri=self.redirect_uri)
        token = oauth.fetch_token(self.token_url, client_secret=self.client_secret, authorization_response=authorization_response)
        return token

    def get_user_info(self, token):
        oauth = OAuth2Session(self.client_id, token=token)
        user_info = oauth.get('https://oauth.cmu.ac.th/userinfo').json()
        return user_info

    def is_cmu_student(self, user_info):
        return user_info.get('affiliation') == 'student'
