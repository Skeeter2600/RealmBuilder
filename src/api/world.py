import json

from flask_restful import Resource, reqparse
import src.components.worlds


class WorldManagement(Resource):

    def put(self):
        """
        This will edit a world's info
        """
        parser = reqparse.RequestParser()
        parser.add_argument('world_id', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('details', type=json)
        args = parser.parse_args()

        world_id = args['world_id']
        user_id = args['user_id']
        session_key = args['session_key']
        details = args['details']

        outcome = src.components.worlds.edit_world(world_id, user_id, session_key, details)

        if outcome[0]:
            return src.components.worlds.get_world_details(world_id, user_id, session_key)

        return outcome[0]

    def post(self):
        """
        This will create a new world
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('owner_id', type=int)
        parser.add_argument('session_key', type=str)
        args = parser.parse_args()

        name = args['name']
        owner_id = args['owner_id']
        session_key = args['session_key']

        outcome = src.components.worlds.add_world(name, owner_id, session_key)

        if outcome[0]:
            return src.components.worlds.get_world_details(outcome[1], owner_id, session_key)

        return outcome[0]

    def delete(self):
        """
        This will delete a world that an owner owns
        """
        parser = reqparse.RequestParser()
        parser.add_argument('world_id', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        args = parser.parse_args()

        world_id = args['world_id']
        user_id = args['user_id']
        session_key = args['session_key']

        outcome = src.components.worlds.delete_world(world_id, user_id, session_key)

        return outcome


class JoinWorldPublic(Resource):

    def put(self):
        """
        This will have a user join a public world
        """
        parser = reqparse.RequestParser()
        parser.add_argument('world_id', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        args = parser.parse_args()

        world_id = args['world_id']
        user_id = args['user_id']
        session_key = args['session_key']

        outcome = src.components.worlds.join_world_public(world_id, user_id, session_key)

        return outcome


class JoinWorldPrivate(Resource):

    def put(self):
        """
        This will have a user join a private world
        """
        parser = reqparse.RequestParser()
        parser.add_argument('world_id', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('admin_id', type=int)
        parser.add_argument('session_key', type=str)
        args = parser.parse_args()

        world_id = args['world_id']
        user_id = args['user_id']
        admin_id = args['admin_id']
        session_key = args['session_key']

        outcome = src.components.worlds.join_world_private(world_id, user_id, admin_id, session_key)

        return outcome


class WorldOwner(Resource):

    def get(self, world_id):
        """
        This will retrieve the info of a world owner
        """
        return src.components.worlds.get_owner(world_id)


class WorldUserList(Resource):

    def get(self, user_id, session_key, world_id):
        """
        This will get the list of users in a world
        """
        return src.components.worlds.get_world_user_list(world_id, user_id, session_key)


class WorldDetails(Resource):

    def get(self, user_id, session_key, world_id):
        """
        This will get the info on a world
        """
        return src.components.worlds.get_world_details(world_id, user_id, session_key)


class WorldSearch(Resource):

    def get(self, user_id, session_key, param, limit, page):
        """
        This will search a world by the defined parameters
        """
        return src.components.worlds.search_world(param, limit, page, user_id, session_key)


