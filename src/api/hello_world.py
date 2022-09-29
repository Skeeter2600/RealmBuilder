from flask_restful import Resource


class HelloWorld(Resource):

    def get(self):
        return dict({'message': 'Hello, World!'})
