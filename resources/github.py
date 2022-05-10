from flask import g, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from ao import github
from libs.strings import gettext
from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


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
    @jwt_required(fresh=True)
    def put(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_username(user_data.username)

        if not user:
            return {"message": gettext("user_not_found")}, 400

        user.password = user_data.password
        user.save_to_db()

        return {"message": gettext("user_password_updated")}, 201
