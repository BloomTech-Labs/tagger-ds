# Imports
from classes.basilica_functions import BasilicaAPI
from flask import Flask, request, jsonify
import json
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pickle
from db import DB, User
from decouple import config
import joblib
from io import BytesIO
from sqlalchemy import exists

# Init Flask app, Database, and Basilica functions
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URL")
DB.init_app(app)
with app.app_context():
    DB.create_all()
basilica_client = BasilicaAPI()

@app.route('/train_model', methods=["POST"])
def train_model():
    # Get JSON and convert to DataFrame
    j = json.loads(request.data)
    df = pd.DataFrame(data=j["emails"])

    # Embed emails
    basilica_client.df = df
    df = basilica_client.embed_basilica_to_df()

    # Train model
    X = np.vstack(np.array(df['embedded']))
    y = df["id_email"].values
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X, y)

    # Save/compress model's pickle into the database
    file_obj = BytesIO() 
    joblib.dump(knn, file_obj, compress=3)
    file_obj.seek(0)
    pkl = file_obj.getvalue()

    # Check if user already exists
    db_user = DB.session.query(exists().where(User.email_address == j["address"])).scalar()
    if db_user: 
        # Update pickle if user exists
        db_user.pickle_file = pkl
    else:
        # Make new user if one doesn't exist
        db_user = User(email_address=j["address"], pickle_file=pkl)
        DB.session.add(db_user)
    DB.session.commit()
    file_obj.close()
    return "Trained a model!"


@app.route("/predict", methods=["GET"])
def predict():
    # Get JSON and convert to DataFrame
    j = json.loads(request.data)
    df = pd.DataFrame(data=j["emails"])

    # Check if user already exists
    db_user = DB.session.query(exists().where(User.email_address == j["address"])).scalar()
    if db_user: 
        # Load pickle and get predictions
        basilica_client.df = df
        df = basilica_client.embed_basilica_to_df()
        file_obj = BytesIO(db_user.pickle_file)
        pkl = joblib.load(file_obj)
        res = pkl.kneighbors(np.vstack(np.array(df['embedded'])), n_neighbors=5)[1][0]
        file_obj.close()
        return json.dumps({"prediction": [str(i) for i in res]})
    else:
        # Return error
        return "No model in database for {}...".format(j["address"])

if __name__ == "__main__":
    app.run()

