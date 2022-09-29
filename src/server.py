from flask import Flask
from flask_restful import Resource, Api
from api.hello_world import HelloWorld
from api.user import UserAccountPublic, AccountInfo, LoginLogout, UserSearch

app = Flask(__name__)
api = Api(app)

api.add_resource(HelloWorld, '/')
api.add_resource(UserAccountPublic, f'/user/<int:user_id>')
api.add_resource(AccountInfo, '/user/')
api.add_resource(LoginLogout, '/log')
api.add_resource(UserSearch, '/search/users/<string:param>/<int:limit>/<int:page>/')

if __name__ == '__main__':
    app.run(debug=True)
    