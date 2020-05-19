from flask import Flask

def create_app():
    """ Initialize the application """
    app = Flask(__name__)

    with app.app_context():
        # Include routes
        from . import routes

        return app
