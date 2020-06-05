# Core imports
import re
import json
import base64
from collections import Counter
# Parsing
import pandas as pd
from bs4 import BeautifulSoup
# Google API
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
# NLP
import nltk
import spacy
from gensim.corpora import Dictionary
from spacy.lang.en.stop_words import STOP_WORDS
from gensim.models.ldamulticore import LdaMulticore


def preprocess_string(text: str) -> str:
    """Process a string for purpose of tagging.

    Args:
        text (string): The email parsed email body.

    Returns:
        text (string): The processed string.
    """
    text = text.strip().lower()
    text = text.replace(
        '[^a-zA-Z\s]', ''
    ).replace(
        '\s+', ' '
    )
    return text


def tokenize_string(text: str, nlp) -> list:
    """Generate tokens for a given body of text.

    Args:
        text (string): Processed body of text
        nlp: Spacy en_core_web_sm model.

    Returns:
        tokens (list): List of tokens
    """
    tokens = list()
    for doc in nlp.pipe(text, batch_size=500):
        doc_tokens = []
        for token in doc:
            if (token.is_stop is False) & (token.is_punct is False):
                doc_tokens.append(token.lemma_.lower())
        tokens.append(doc_tokens)
    return tokens


def generate_tags(tokens: list) -> list:
    """Perform LDA Topic Modelling to aquire tags.

    Args:
        tokens (list): List of tokens

    Returns:
        tags_list (list) List of appropriate tags for
        given tokens.
    """
    id2word = Dictionary(tokens)
    corpus = [id2word.doc2bow(d) for d in tokens]
    model = LdaMulticore(
        corpus=corpus,
        id2word=id2word,
        random_state=42,
        num_topics=10,
        passes=2,
        workers=1
    )
    words = [re.findall(r'"([^"]*)"', t[1]) for t in model.print_topics()]
    wordcount = Counter(words[0] + words[1] + words[2] + words[3] + words[4])
    tags = pd.DataFrame.from_dict(
        wordcount, orient='index', columns=['number']
        )
    tags = tags.drop(tags[tags['number'] <= 1].index)
    tags = tags.sort_values(by=['number'], ascending=False).T
    tags_list = [word for word in tags.columns]

    return tags_list


def build_service(info: dict):
    """Function to build the Resource object.

    Args:
        info (dict): Token containing valid user auth
        refresh token, client_id, and client_secret

    Returns:
        service (googleapiclient.discovery.Resource)

    Example:
        >>> info = {
        ...     refresh_token: "my_refresh_token_hash",
        ...     client_id: "aW82nG-so_client_id",
        ...     client_secret: "super_secret_hash"
        ... }
        >>> service = build_service(info)
        >>> type(service)
        <class 'googleapiclient.discovery.Resource'>
    """
    creds = Credentials.from_authorized_user_info(info)
    service = build('gmail', 'v1', credentials=creds)
    return service


def user_emails(service, recent_id=None) -> list:
    """Retrieve user emails.

    Args:
        service (googleapiclient.discovery.Resource):
        Resource object that will be used to obtain the
        list of emails.

        recent_id (string): The most recent id to begin pulling
        emails from. None by default, which will pull all emails.

    Returns:
        emails (list): A list that contains each requested email id.
    """
    email_list = list()
    # Grab first page of emails ids
    emails = service.users().messages().list(
            userId='me'
        ).execute()
    email_list = [x['id'] for x in emails['messages']]
    while "nextPageToken" in emails.keys():
        if recent_id in email_list:
            break
        else:
            emails = service.users().messages().list(
                    userId='me', pageToken=emails['nextPageToken']
                ).execute()

    if recent_id is not None:
        idx = email_list.index(recent_id)
        email_list = email_list[:idx]
    return email_list


def generate_emails(service, id_list):
    """Generator object yielding individual emails.

    Args:
        service (googleapiclient.discovery.eesource):
        Resource Object used to query the GMail API
        for an authorized user.

        id_list (list): List of email ids that will
        be passed into the api queries.

    Returns:
        Generator that yields each individual email.
    """
    generator = (
            service.users().messages().get(
                userId='me', id=x
                ).execute()
            for x in id_list
            )
    return generator


def generate_tagged_emails(service, email_gen):
    """Tag recent emails

    Args:
        service (googleapiclient.discovery.Resource):
        Resource to query the GMail API.

        email_gen (generator): Generator that supplies
        each email for the user.

    Yields:
        email (dict): Dictionary containing the email data.
    """

    nlp = spacy.load("en_core_web_sm")
    stopwords = STOP_WORDS  # Stop words

    for email in email_gen:

        # Begin tagging logic
        message_payload = email['payload']

        if message_payload['mimeType'] == "text/plain":
            message_body = message_payload['body']['data']
        elif message_payload['mimeType'] == "multipart/alternative":
            message_body = message_payload['parts'][1]['body']['data']
        elif message_payload['mimeType'] == "multipart/related":
            message_body = message_payload['parts'][0]['parts'][1]['body']['data']
        else:
            message_body = message_payload['parts'][1]['body']['data']

        message_text = base64.urlsafe_b64decode(message_body.encode('utf-8'))
        text = re.sub(
            r"https\S+", "", str(
                BeautifulSoup(message_text, 'html.parser').text
            )
        )

        text = preprocess_string(text)
        tokens = tokenize_string(text, nlp)
        tags_list = generate_tags(tokens)

        email['smartTags'] = [word for word in tags_list]

        yield json.dumps(email)
