from flask import g, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from ao import github
from models.user import UserModel


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(callback="http://localhost:5000/login/github/authorized")


class GithubAuthorized(Resource):
    @classmethod
    def get(cls):
        rep = github.authorized_response()

        if rep is None or 'access_token' not in rep:
            return {
                'error': request.args['error'],
                'error_description': request.args['error_description']
            }

        g.access_token = rep['access_token']
        oauth_rep = github.get("user")
        # token = rep['access_token']
        # oauth_rep = github.get("user", token=token)
        username = oauth_rep.data['login']

        user = UserModel.find_by_username(username)
        if user is None:
            user = UserModel(username=username, password="")
            user.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


class SetPassword(Resource):
    @classmethod
    def put(cls):
        user_data = request.get_data()

        return user_data
