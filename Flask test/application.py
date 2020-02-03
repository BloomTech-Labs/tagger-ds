"""Flask App for Predicting Optimal AirBnB prices in Berlin"""
from flask import Flask

# create app:
def create_app():
    APP = Flask(__name__)

    @APP.route('/', methods=['GET'])
    def test():
        return "Hello World!"

    return APP
