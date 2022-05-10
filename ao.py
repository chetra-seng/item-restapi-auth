import os

from flask import g
from flask_oauthlib.client import OAuth

oauth = OAuth()
github = oauth.remote_app(
    name='github',
    base_url="https://api.github.com",
    request_token_url=None,
    request_token_params={'scope': 'user:email'},
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_method="POST",
    authorize_url='https://github.com/login/oauth/authorize',
    app_key='GITHUB'
)

@github.tokengetter
def get_github_accesstoken():
    if 'access_token' in g:
        return g.access_token
