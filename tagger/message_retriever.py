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
from flask import jsonify

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

previous_email_pull = '172317ca92683d33'

def user_emails(creds):
    """ Pulls user emails """

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    emails = service.users().messages().list(userId='me').execute()

    return emails

def recent_id(emails):
    # Find most recent message
    recent_msg_id = emails['messages'][0]['id']
    return recent_msg_id


def tag_recent(recent_msg_id, creds):
    """ Generates tags on the most recent email """

    # Build service
    service = build('gmail', 'v1', credentials=creds)

    # PRINT 1
    print("Getting most recent message...")

    # Call message content
    message_content = service.users().messages().get(
        userId='me', id=recent_msg_id).execute()

    # Call message body
    message_payload = message_content['payload']
    if "parts" in message_payload:
        message_body = message_content['payload']['parts']
        message_body_dict = dict(message_body[0])
    else:
        message_body = message_content['payload']['body']['data']
        message_body_dict = dict(message_body[0])

    # PRINT 2
    print("Most recent message obtained. Decoding...")

    # Decode base64 encoding
    decode = message_body_dict['body']['data']
    decodedContents = base64.urlsafe_b64decode(decode.encode('utf-8'))

    # Clean the text
    text = BeautifulSoup(decodedContents, 'html.parser')
    text = str(text.text)
    text = re.sub(r"http\S+", "", text)
    text = [text]

    # PRINT 3
    print("Decoded message body. Loading spacy small model...")

    # Load spacy model
    nlp = spacy.load('en_core_web_sm')

    # PRINT 4
    print("Spacy model loaded. Creating stop words list...")

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
    # stop = stopwords.words('english')

    # PRINT 4
    print("Generating email dataframe...")

    # Shape text & tokenize
    df = pd.DataFrame(text, columns = ['email_body'])

    #remove whitespace
    df['email_body'] = df['email_body'].str.strip().str.lower()

    #Start with date
    df['email_body'].str.match('\d?\d/\d?\d/\d{4}').all()

    #Replace all non-overlapping matches
    df['email_body'] = df['email_body'].str.replace('[^a-zA-Z\s]', '').str.replace('\s+', ' ')

    # PRINT 5
    print("Tokenizing data...")

    # Generate NLP model
    tokens = []
    for doc in nlp.pipe(df['email_body'], batch_size=500):
        doc_tokens = []
        for token in doc:
            if (token.is_stop is False) & (token.is_punct is False):
                doc_tokens.append(token.lemma_.lower())
        tokens.append(doc_tokens)
    df['tokens'] = tokens

    # PRINT 6
    print("Modelling token data for Topics with LDA...")

    # Topic Modelling
    id2word = Dictionary(df['tokens'])
    corpus = [id2word.doc2bow(d) for d in df['tokens']]
    model = LdaMulticore(corpus=corpus,
                         id2word=id2word,
                         random_state=42,
                         num_topics=10,
                         passes=1,
                         workers=1)

    # PRINT 7
    print("Building tag list...")

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
    email_tags = {'tokens':[word for word in tags_list]}
    email = {'email':decode, 'tokens':[word for word in tags_list]}

    # PRINT 8
    print("Complete, returning json...")

    # Return sorted smart tag list
    return jsonify(email)

# # Recent messages list
# message_tally = []
# for _ in range(len(message['messages'])):
#     message_tally.append(message['messages'][_]['id'])
#     if message['messages'][_]['id'] == previous_email_pull:
#         break
