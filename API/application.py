from flask import Flask, request, jsonify
from joblib import load
from nltk.tokenize.regexp import regexp_tokenize
from main import clean_text, tokenize, getTags
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
import nltk
import pickle


# Found solution at https://stackoverflow.com/questions/50465106/attributeerror-when-reading-a-pickle-file
class MyCustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "__main__":
            module = "application"
        return super().find_class(module, name)

with open('vect.pkl', 'rb') as f:
    unpickler = MyCustomUnpickler(f)
    vect = unpickler.load()

application = Flask(__name__)

lemmatizer = WordNetLemmatizer()
tokeni_zer = tokenize
encoder = load('labeller.pkl')
model = load('randomforest.pkl')
personal_model = load('logreg.pkl')
personal_vect = load('basic_tfidf.pkl')

def tag_email(text):
    text = vect.transform([text])
    pred = model.predict_proba(text)
    new_tag = getTags(pred[0], encoder)
    return new_tag

@application.route('/')
def home():
    return 'You made it'

@application.route('/personal', methods=['POST'])
def personal():
    data = request.get_json()
    uid = data['id']
    sender = data['sender']
    subject = data['subject']
    message = data['message']
    text = sender + ' ' + subject + ' ' + message
    text_clean = clean_text(text)
    text_vect = personal_vect.transform([text_clean])
    predict = personal_model.predict(text_vect)
    print(predict[0])
    email = {'message-id': uid, 'from': sender, 'subject': subject,
             'message': message, 'personal': predict.tolist()}
    
    return jsonify(email)

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
                    'message': message, 'tag': tag}
    
    return jsonify(tagged_email)


if __name__ == "__main__":
    application.run()