# REST API for AI Project - CS464
# Written by Nate Arkin and Max Herrick

from flask import Flask, send_file, abort
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def get(self):
        data = pd.read_csv('TestData.csv')
        data = data.to_dict()
        return {'data': data}, 200

api.add_resource(Test, '/test')

class MainPage(Resource):
    def get(self):
        try:
            return send_file('Web/index.html')
        except FileNotFoundError:
            abort(404)

api.add_resource(MainPage, '/')

class DownloadDataset(Resource):
    def get(self):
        try:
            return send_file('Dataset/train.csv', as_attachment=True)
        except FileNotFoundError:
            abort(404)

api.add_resource(DownloadDataset, '/DownloadTrainData')

class FeaturesUI(Resource):
    def get(self):
        try:
            return send_file('Web/FeaturesUI.html')
        except FileNotFoundError:
            abort(404)

api.add_resource(FeaturesUI, '/FeaturesUI')

if __name__ == '__main__':
    app.run()