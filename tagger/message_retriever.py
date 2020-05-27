# Email Retrieving Gateway
#
# TODO OOP
#
# Current build is proof of concept for retrieving email from gmail account.
# Retrieves 1 email at a time. Next iteration will retrieve all emails since
# last known retrieved pulldown.

# Module imports / focused on Google API
import base64
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
from collections import Counter
from googleapiclient.discovery import build
from gensim.corpora import Dictionary
from gensim.models.ldamulticore import LdaMulticore
from gensim.models.coherencemodel import CoherenceModel
import spacy
import nltk
import string
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

previous_email_pull = '172317ca92683d33'

def load_user_token(token):
    """ Loads user token """

    user_token = json.loads(token)
    return user_token

def main():
    creds = None
    with open('token.pickle', 'rb') as f:
        data = pickle.load(f)
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # In production this authorization method will be handled through a JSON
    # retrieved from the BE server.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)


    # Call the Gmail API
    message = service.users().messages().list(userId='me').execute()

    # Find most recent message
    recent_msg_id = message['messages'][0]['id']
    #print(recent_msg_id)
    # Recent messages list
    message_tally = []
    for _ in range(len(message['messages'])):
        message_tally.append(message['messages'][_]['id'])
        if message['messages'][_]['id'] == previous_email_pull:
            break

    # Call message content
    message_content = service.users().messages().get(
        userId='me', id=recent_msg_id).execute()
    #print(message_content)
    # Call message body
    message_body = message_content['payload']['parts']
    #message_body = message_content['payload']
    message_body_dict = dict(message_body[0])
    #print("Message Body Dict:", message_body_dict)

    # Decode base64 encoding
    decode = message_body_dict['body']['data']
    decodedContents = base64.urlsafe_b64decode(decode.encode('ASCII'))
    #print(decodedContents)

    # Clean the text
    text = BeautifulSoup(decodedContents, 'html.parser')
    text = str(text.text)
    text = re.sub(r"http\S+", "", text)
    text = [text]

    # Output

    # Load spacy model
    nlp = spacy.load('en_core_web_md')

    my_stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours',
                 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
                 "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself',
                 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
                 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am',
                 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
                 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
                 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
                 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
                 'into', 'through', 'during', 'before', 'after', 'above', 'below',
                 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
                 'again', 'further', 'then', 'once', 'here', 'there', 'when',
                 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
                 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
                 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
                 'can', 'will', 'just', 'don', "don't", 'should', "should've",
                 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
                 "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn',
                 "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven',
                 "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't",
                 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
                 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren',
                 "weren't", 'won', "won't", 'wouldn', "wouldn't", "unsubscribe",
                 "st"]

    STOP_WORDS = nlp.Defaults.stop_words.union(my_stop_words)

    stop = stopwords.words('english')

    # Shape text & tokenize
    df = pd.DataFrame(text, columns = ['email_body'])

    #remove whitespace
    df['email_body'] = df['email_body'].str.strip().str.lower()

    #Start with date
    df['email_body'].str.match('\d?\d/\d?\d/\d{4}').all()

    #Replace all non-overlapping matches
    df['email_body'] = df['email_body'].str.replace('[^a-zA-Z\s]', '').str.replace('\s+', ' ')

    # Generate NLP model
    tokens = []
    for doc in nlp.pipe(df['email_body'], batch_size=500):
        doc_tokens = []
        for token in doc:
            if (token.is_stop is False) & (token.is_punct is False):
                doc_tokens.append(token.lemma_.lower())
        tokens.append(doc_tokens)
    df['tokens'] = tokens

    id2word = Dictionary(df['tokens'])

    # Remove extremes
    # Deprecated for tagger email / not useful in single emails
    #id2word.filter_extremes(no_below=5, no_above=.98)

    corpus = [id2word.doc2bow(d) for d in df['tokens']]

    model = LdaMulticore(corpus=corpus,
                         id2word=id2word,
                         random_state=42,
                         num_topics=10,
                         passes=8,
                         workers=12)

    # Generate topics from model
    words = [re.findall(r'"([^"]*)"', t[1]) for t in model.print_topics()]

    # Count instances of each word seeking weight of dupes
    wordcount = Counter(words[0] + words[1] + words[2] + words[3] + words[4])

    # Generate dataframe of results, drop those found less than twice, sort descending
    tags = pd.DataFrame.from_dict(wordcount, orient='index', columns=['number'])
    tags.drop(tags[tags.number <= 1].index, inplace=True)
    tags.sort_values(by=['number'], ascending=False, inplace=True)
    tags['length'] = range(len(tags))
    tags = tags.T
    tags_list = tags.columns

    # Return sorted smart tag list
    return(tags_list)


    # topics = [' '.join(t[0:9]) for t in words]
