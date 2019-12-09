from flask import Flask, request, jsonify
from joblib import load
from nltk.tokenize.regexp import regexp_tokenize
from main import clean_text, tokenize
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