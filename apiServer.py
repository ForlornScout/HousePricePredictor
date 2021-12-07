# REST API for AI Project - CS464
# Written by Nate Arkin and Max Herrick

from flask import Flask, send_file, abort, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
from sklearn import tree
import ast

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def get(self):
        print(request.form)
        print(request.form["test"])
        return request.form

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
        print(request.data)
        try:
            return send_file('Web/FeaturesUI.html')
        except FileNotFoundError:
            abort(404)

api.add_resource(FeaturesUI, '/FeaturesUI')

class JQUERY(Resource):
    def get(self):
        try:
            return send_file('Web/jquery-3.6.0.min.js')
        except FileNotFoundError:
            abort(404)

api.add_resource(JQUERY, '/JQuery_FILE')

class getSimilarHouses(Resource):
    def post(self):
        featuresRequired = {}
        
        for key in request.form:
            if key == 'noBedrooms':
                featuresRequired["BedroomAbvGr"] = int(request.form['noBedrooms'])
            elif key == 'noFullBaths':
                featuresRequired["FullBath"] = int(request.form['noFullBaths'])
            elif key == 'noHalfBaths':
                featuresRequired["HalfBath"] = int(request.form['noHalfBaths'])
            elif key == 'noCarGarage':
                featuresRequired["GarageCars"] = int(request.form['noCarGarage'])
            elif key == 'overallQuality':
                featuresRequired["OverallQual"] = int(request.form['overallQuality'])
            elif key == 'overallCond':
                featuresRequired["OverallCond"] = int(request.form['overallCond'])

            # print(featuresRequired)

        data = pd.read_csv('Dataset/train.csv')
        data['MatchRating'] = 0
        for index in data.index:
            for key in featuresRequired:
                if data.loc[index,key] == featuresRequired[key]:
                    data.loc[index,'MatchRating'] = data.loc[index,'MatchRating']+1
        data = data[data.MatchRating > 0]
        data.sort_values(by=['MatchRating'], inplace=True, ascending=False)
        data = data.head(5)
        
        # print(data.to_json(orient="records"))
        return data.to_json(orient="records")

api.add_resource(getSimilarHouses, '/api/getSimilarHouses')

class getHousePrice(Resource):
    def post(self):
        featuresRequired = {}
        
        for key in request.form:
            if key == 'noBedrooms':
                featuresRequired["BedroomAbvGr"] = int(request.form['noBedrooms'])
            elif key == 'noFullBaths':
                featuresRequired["FullBath"] = int(request.form['noFullBaths'])
            elif key == 'noHalfBaths':
                featuresRequired["HalfBath"] = int(request.form['noHalfBaths'])
            elif key == 'noCarGarage':
                featuresRequired["GarageCars"] = int(request.form['noCarGarage'])
            elif key == 'overallQuality':
                featuresRequired["OverallQual"] = int(request.form['overallQuality'])
            elif key == 'overallCond':
                featuresRequired["OverallCond"] = int(request.form['overallCond'])

        data = pd.read_csv('Dataset/train.csv')
        x = data[['BedroomAbvGr', 'FullBath', 'HalfBath', 'GarageCars', 'OverallQual', 'OverallCond']]
        y = data[['SalePrice']]
        classifier = tree.DecisionTreeClassifier()
        classifier.fit(x, y)

        predictionData = {}
        for key in ['BedroomAbvGr', 'FullBath', 'HalfBath', 'GarageCars', 'OverallQual', 'OverallCond']:
            found = False
            for feature in featuresRequired:
                if key == feature:
                    predictionData[feature] = featuresRequired[key]
                    found = True
            if not found:
                predictionData[key] = data[key].mean()
        prediction = pd.DataFrame(predictionData, index=[0])
        predictedPrice = classifier.predict(prediction)
        print(predictionData)
        return int(predictedPrice[0])

api.add_resource(getHousePrice, '/api/getHousePrice')

if __name__ == '__main__':
    app.run(port=5002)