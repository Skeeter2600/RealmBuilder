import json

from flask_restful import Resource, reqparse
import src.components.specials


class SpecialManagement(Resource):

    def put(self):
        """
        This will edit a special's info
        """
        parser = reqparse.RequestParser()
        parser.add_argument('world_id', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('special_id', type=int)
        parser.add_argument('details', type=json)
        args = parser.parse_args()

        world_id = args['world_id']
        user_id = args['user_id']
        session_key = args['session_key']
        special_id = args['special_id']
        details = args['details']

        outcome = src.components.specials.edit_special(user_id, session_key, special_id, world_id, details)

        if outcome[0]:
            return src.components.specials.get_special_info(user_id, session_key, special_id, True)

        return outcome[0]

    def post(self):
        """
        This will create a new special
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('details', type=str)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']
        details = args['details']

        outcome = src.components.specials.add_special(user_id, session_key, details)

        if outcome[0]:
            return src.components.specials.get_special_info(user_id, session_key, outcome[1], True)

        return outcome[0]

    def delete(self):
        """
        This will delete a special that a user owns
        """
        parser = reqparse.RequestParser()
        parser.add_argument('special_id', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('world_id', type=int)
        args = parser.parse_args()

        special_id = args['special_id']
        user_id = args['user_id']
        session_key = args['session_key']
        world_id = args['world_id']

        outcome = src.components.specials.delete_special(user_id, session_key, special_id, world_id)

        return outcome


class CopySpecial(Resource):

    def post(self, special_id):
        """
        This will make a copy of a special
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('world_id', type=int)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']
        world_id = args['world_id']

        outcome = src.components.specials.copy_special(user_id, session_key, special_id, world_id)

        if outcome[0]:
            return src.components.specials.get_special_info(user_id, session_key, outcome[1], True)

        return outcome[0]


class RevealSpecial(Resource):

    def put(self, world_id, special_id):
        """
        This will reveal hidden info for a special
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']

        return src.components.specials.reveal_hidden_special(user_id, session_key, world_id, special_id)


class SpecialDetails(Resource):

    def get(self, special_id):
        """
        This will get the info on a special
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('admin', type=bool)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']
        admin = args['admin']

        return src.components.specials.get_special_info(special_id, user_id, session_key, admin)



