import json

from flask_restful import Resource, reqparse
import src.components.users


class UserAccountPublic(Resource):
    def get(self, user_id):
        """
        This will retrieve the info of a user
        """
        return src.components.users.get_user_public(user_id)


class AccountInfo(Resource):
    def put(self):
        """
        This will edit a user's profile
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('details', type=json)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']
        details = args['details']

        outcome = src.components.users.edit_account(user_id, session_key, details)

        if outcome:
            return src.components.users.get_user_private(user_id, session_key)

        return outcome

    def post(self):
        """
        This will create a new user
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()

        username = args['username']
        password = args['password']
        email = args['email']

        outcome = src.components.users.create_user(username, password, email)

        if outcome == "Success!":
            return src.components.users.login_user(username, password)

        return outcome

    def delete(self):
        """
        This will delete a user's account
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']

        outcome = src.components.users.delete_user(user_id, session_key)

        return outcome


class UserAccountPrivate(Resource):
    def get(self, user_id, session_key):
        """
        This will get a user's private profile
        """
        outcome = src.components.users.get_user_private(user_id, session_key)

        return outcome


class Login(Resource):
    def get(self, username, password):
        return src.components.users.login_user(username, password)


class Logout(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']

        outcome = src.components.users.logout_user(user_id, session_key)
        return outcome


class UserSearch(Resource):

    def get(self, user_id, session_key, param, limit, page):
        return src.components.users.search_user(param, limit, page, user_id, session_key)

