# app.py - a minimal flask api using flask_restful
import routes

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

api.add_resource(routes.MainPage, '/')
api.add_resource(routes.Stats, '/stats')
api.add_resource(routes.News, '/news')
api.add_resource(routes.Cities, '/cities')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

