from flask import Flask, request, jsonify
from joblib import load


application = Flask(__name__)
model = load('model1.joblib')
vect = load('vect1.joblib')

def tag_email(text):
    text = vect.transform([text])
    tag = model.predict(text)
    return tag

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
    
    return tagged_email


if __name__ == "__main__":
    application.run()
