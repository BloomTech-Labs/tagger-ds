from flask import Flask
from flaskext.markdown import Markdown

md = Markdown()

def create_app():
    """ Initialize the application """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Application plugins
    md.init_app(app)

    with app.app_context():
        # Include routes
        from . import routes

        return app
