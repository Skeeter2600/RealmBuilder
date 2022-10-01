import json

from flask_restful import Resource, reqparse
import src.components.cities


class CityManagement(Resource):

    def put(self):
        """
        This will edit a city's info
        """
        parser = reqparse.RequestParser()
        parser.add_argument('world_id', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('city_id', type=int)
        parser.add_argument('details', type=json)
        args = parser.parse_args()

        world_id = args['world_id']
        user_id = args['user_id']
        session_key = args['session_key']
        city_id = args['city_id']
        details = args['details']

        outcome = src.components.cities.edit_city(user_id, session_key, city_id, world_id, details)

        if outcome[0]:
            return src.components.cities.get_city(user_id, session_key, city_id, True)

        return outcome[0]

    def post(self):
        """
        This will create a new city
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('details', type=str)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']
        details = args['details']

        outcome = src.components.cities.add_city(user_id, session_key, details)

        if outcome[0]:
            return src.components.cities.get_city(user_id, session_key, outcome[1], True)

        return outcome[0]

    def delete(self):
        """
        This will delete a special that a user owns
        """
        parser = reqparse.RequestParser()
        parser.add_argument('city_id', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('world_id', type=int)
        args = parser.parse_args()

        city_id = args['city_id']
        user_id = args['user_id']
        session_key = args['session_key']
        world_id = args['world_id']

        outcome = src.components.cities.delete_city(user_id, session_key, city_id, world_id)

        return outcome


class CopyCity(Resource):

    def post(self, city_id):
        """
        This will make a copy of a city
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('world_id', type=int)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']
        world_id = args['world_id']

        outcome = src.components.cities.copy_city(user_id, session_key, city_id, world_id)

        if outcome[0]:
            return src.components.cities.get_city(user_id, session_key, outcome[1], True)

        return outcome[0]


class CityDetails(Resource):

    def get(self, city_id):
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

        return src.components.cities.get_city(city_id, user_id, session_key, admin)


class CitySearch(Resource):

    def get(self, world_id, param, limit, page):
        """
        This will search a special by the defined parameters
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']

        return src.components.cities.search_for_city(param, world_id, limit, page, user_id, session_key)
