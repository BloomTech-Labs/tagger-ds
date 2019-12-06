from flask import Flask, request, jsonify
from joblib import load
from nltk.tokenize.regexp import regexp_tokenize
from functions import clean_text, regnltk_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
import nltk
# nltk.download('wordnet')


application = Flask(__name__)

lemmatizer = WordNetLemmatizer()
vect = load('vect.joblib')
encoder = load('labeller.joblib')
model = load('randomforest.joblib')

def tag_email(text):
    text = vect.transform([text])
    tag = model.predict(text)
    new_tag = encoder.inverse_transform(tag)
    return new_tag

@application.route('/')
def home():
    return 'You made it'

@application.route('/api/tags', methods=['POST'])
def api():
    data = request.get_json()
    uid = data['id']
    sender = data['sender']
    subject = data['subject']
    message = data['message']
    text = sender + ' ' + subject + ' ' + message
    tag = tag_email(text)
    tagged_email = {'message-id': uid, 'from': sender, 'subject': subject,
                    'message': message, 'tag': tag[0]}
    
    return jsonify(tagged_email)


if __name__ == "__main__":
    application.run()