from __future__ import absolute_import, division, print_function, unicode_literals
import json
import pickle
import numpy as np
from flask import Flask, request, jsonify
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import tensorflow as tf
from tensorflow.keras.models import model_from_json, Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from functions import clean_text, get_tags, format_inputs


# Tensorflow session
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

app = Flask(__name__)

#---------------------------------------------
# Loading Tokenizer, LSTM_model, and LSTM_weights
with open('final_tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

json_file = open('combined_model2.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# loaded_model.make_predict_function()

loaded_model.load_weights("combined_weights2.h5")
print("Loaded model from disk")

# Loading Personal model and vect
personal_model = load('logreg.pkl')

personal_vect = load('basic_tfidf.pkl')
#---------------------------------------------

@app.route('/')
def home():
    return 'You made it'

@app.route('/api/tags', methods=['POST'])
def api():
    """
    API to take in email data (sender, subject, message)
    Cleans, vectorizes, and formats text for LSTM model
    Predicts labels for email tags
    Repeats the cleaning and vectorizing to predict for 'Personal' tag
    """
    # Email data split up and cleaned/formatted
    data = request.get_json()
    uid = data['id']

    sender = data['sender']
    sender_format = format_inputs(sender, 100)

    subject = data['subject']
    subject_format = format_inputs(subject, 150)

    message = data['message']
    message_format = format_inputs(message, 5000)

    # Model takes three different inputs from the different sections
    text = [message_format, subject_format, sender_format]

    # Prediction model for tags
    tag = get_tags(text, loaded_model)

    # Set up text for 'Personal' model
    personal_text = sender + ' ' + subject + ' ' + message
    clean_personal_text = clean_text(personal_text)
    clean_personal_vect = personal_vect.transform([clean_personal_text])

    # Predict 'Personal' tags
    personal_tag = personal_model.predict(clean_personal_vect)

    # JSON output of predictions
    tagged_email = {'message-id': uid, 'from': sender, 'subject': subject,
                    'message': message, 'tag': tag, 'personal':personal_tag.tolist()}
    
    return json.dumps(tagged_email)


if __name__ == "__main__":
    app.run(debug=True)