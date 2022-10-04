import json

from flask_restful import Resource, reqparse
import src.components.comments


class CommentManagement(Resource):

    def put(self):
        """
        This will edit an comment's info
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('comment_id', type=int)
        parser.add_argument('comment', type=json)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']
        comment_id = args['comment_id']
        comment = args['comment']

        outcome = src.components.comments.edit_comment(user_id, session_key, comment_id, comment)

        if outcome[0]:
            return src.components.comments.get_comment(comment_id)

        return outcome[0]

    def post(self):
        """
        This will create a new comment
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=str)
        parser.add_argument('world_id', type=int)
        parser.add_argument('component_id', type=int)
        parser.add_argument('component_type', type=str)
        parser.add_argument('comment', type=str)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']
        world_id = args['world_id']
        component_id = args['component_id']
        component_type = args['component_type']
        comment = args['comment']

        outcome = src.components.comments.add_comment(user_id, session_key, world_id, component_id, component_type, comment)

        if outcome[0]:
            return src.components.comments.get_comment(outcome[1])
        return outcome[0]

    def delete(self):
        """
        This will delete a comment that a user owns
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('session_key', type=int)
        parser.add_argument('comment_id', type=int)
        args = parser.parse_args()

        user_id = args['user_id']
        session_key = args['session_key']
        comment_id = args['comment_id']

        outcome = src.components.comments.delete_comment(user_id, session_key, comment_id)

        return outcome


class CommentDetails(Resource):

    def get(self, comment_id):
        """
        This will get the info on an npc
        """
        return src.components.comments.get_comment(comment_id)


class ComponentComments(Resource):

    def get(self, component_table, comment_id):
        """
        This will get the comments for a component
        """
        return src.components.comments.get_component_comments(comment_id, component_table)


class UserComments(Resource):
    def get(self, user_id, limit, page):
        """
        This will get the comments that a user has posted
        """
        return src.components.comments.get_user_comments(user_id, limit, page)
