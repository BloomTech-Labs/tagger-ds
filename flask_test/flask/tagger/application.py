from flask import Flask

def create_app():
    APP = Flask(__name__)

    @APP.route('/', methods=['GET'])
    def test():
        return "Hello World!"

    return APP
