from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    email_address = DB.Column(DB.Text(), nullable=False, primary_key=True)
    pickle_file = DB.Column(DB.LargeBinary(), nullable=False)
    uids = DB.Column(DB.LargeBinary(), nullable=False)
    dtype = DB.Column(DB.Text(), nullable=False)