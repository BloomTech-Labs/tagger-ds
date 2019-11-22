import gzip

from flask import Flask, request, jsonify
from joblib import load
from io import StringIO
from boto import connect_s3


#AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

application = Flask(__name__)
#model = load('model1.joblib')
#vect = load('vect1.joblib')

s3 = connect_s3()
b = s3.get_bucket('elasticbeanstalk-us-east-2-896750313793')
k = b.get_key('model1.joblib')
f = gzip.GzipFile(fileobj=StringIO(k.get_contents_as_string()))
model = load(f)

k2 = b.get_key('vect1.joblib')
f2 = gzip.GzipFile(fileobj=StringIO(k.get_contents_as_string()))
vect = load(f2)

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
    tagged_email = {'id': uid, 'sender': sender, 'subject': subject,
                    'message': message, 'tag': tag[0]}
    
    return tagged_email


if __name__ == "__main__":
    application.run()