import click

# from sqlalchemy_utils import database_exists, create_database

# figure out where snakeeeyes comes from
# 
from tagger.application import create_app
# from snakeeyes.extensions import db
from db import DB, User

# Create an app context for the database connection.
app = create_app()
DB.app = app


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@click.command()
def init():
    DB.drop_all()
    DB.create_all()

    return None


@click.command()
@click.pass_context
def reset(ctx):

    ctx.invoke(init)

    return None


cli.add_command(init)
cli.add_command(reset)