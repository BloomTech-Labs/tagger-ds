# Imports
from classes.new_email_functions import IMap
from classes.Basillica import BasilicaAPI
from flask import Flask, request, jsonify
import json
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pickle
from db import DB, User
from decouple import config

# Init Flask app, Database, and Basilica functions
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URL")
DB.init_app(app)
with app.app_context():
    DB.create_all()
basilica_client = BasilicaAPI()

@app.route('/train_model', methods=["POST"])
def train_model():
    j = json.loads(request.data) # Get JSON and convert to DataFrame
    df = pd.DataFrame(data=j["emails"])
    basilica_client.df = df

    df = basilica_client.embed_basilica_to_df() # Embed Emails

    X = np.vstack(np.array(df['embedded'])) # Train Model
    y = df["id_email"].values
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X, y)

    pkl = pickle.dumps(knn) # Save model Pickle into the Database
    db_user = User(email_address=j["address"], pickle_file=pkl)
    DB.session.add(db_user)
    DB.session.commit()
    return "Trained a model!"


if __name__ == "__main__":
    app.run()

