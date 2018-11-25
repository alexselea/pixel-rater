from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

import sys
sys.path.append('image-quality-assessment')
import plates_test

app = Flask(__name__)

api = Api(app)
CORS(app)



@app.route("/", methods = ['POST', 'GET'])
def result():
    # ajunge
    if request.method == 'GET':
        place = request.args.get('place', None)
        if place:
            print("face ceva macar")
            asd = plates_test.places(place)
            print(asd)
            return jsonify(asd)
            

            #process link

            #feed to frontend the images
        return "shit"


@app.route("/result", methods = ['GET'])
def hello():
    return "Hello World!!!!!!!!!!!!!!!!!!!!!!!"


if __name__ == "__main__":
    app.run(debug = True)
