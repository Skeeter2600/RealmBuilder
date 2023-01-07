import json

from flask_restful import Resource, reqparse
import src.components.npcs


class NPCManagement(Resource):

    def put(self):
        """
        This will edit an npc's info
        """
        parser = reqparse.RequestParser()
        parser.add_argument('world_id', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('npc_id', type=int)
        parser.add_argument('details', type=json)
        args = parser.parse_args()

        world_id = args['world_id']
        user_id = args['user_id']
        session_key = args['session_key']
        npc_id = args['npc_id']
        details = args['details']

        outcome = src.components.npcs.edit_npc(user_id, session_key, npc_id, world_id, details)

        if outcome[0]:
            return src.components.npcs.get_npc_info(user_id, session_key, npc_id, True)

        return outcome[0]

    def post(self):
        """
        This will create a new npc
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('details', type=str)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']
        details = args['details']

        outcome = src.components.npcs.add_npc(user_id, session_key, details)

        if outcome[0]:
            return src.components.npcs.get_npc_info(user_id, session_key, outcome[1], True)
        return outcome[0]

    def delete(self):
        """
        This will delete a special that a user owns
        """
        parser = reqparse.RequestParser()
        parser.add_argument('npc_id', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('world_id', type=int)
        args = parser.parse_args()

        npc_id = args['npc_id']
        user_id = args['user_id']
        session_key = args['session_key']
        world_id = args['world_id']

        outcome = src.components.npcs.delete_npc(user_id, session_key, npc_id, world_id)

        return outcome


class CopyNPC(Resource):

    def post(self, npc_id):
        """
        This will make a copy of an npc
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('world_id', type=int)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']
        world_id = args['world_id']

        outcome = src.components.npcs.copy_npc(user_id, session_key, npc_id, world_id)

        if outcome[0]:
            return src.components.npcs.get_npc_info(user_id, session_key, outcome[1], True)

        return outcome[0]


class RevealNPC(Resource):

    def put(self, world_id, npc_id):
        """
        This will reveal hidden info for an npc
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']

        return src.components.npcs.reveal_hidden_npc(user_id, session_key, world_id, npc_id)


class NPCDetails(Resource):

    def get(self, user_id, session_key, npc_id, admin):
        """
        This will get the info on an npc
        """
        return src.components.npcs.get_npc_info(user_id, session_key, npc_id, admin)


class NPCSearch(Resource):

    def get(self, user_id, session_key, world_id,  param, limit, page):
        """
        This will search a special by the defined parameters
        """
        return src.components.npcs.search_for_npc(param, world_id, limit, page, user_id, session_key)


