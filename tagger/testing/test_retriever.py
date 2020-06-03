import pytest
import json
import os
from flask import current_app as app
from flask import request, redirect, render_template, url_for, Response
from markdown import markdown as markd
import markdown.extensions.fenced_code
import markdown.extensions.codehilite
from pygments.formatters import HtmlFormatter
import base64
from bs4 import BeautifulSoup
import re
import pandas as pd
from collections import Counter
from googleapiclient.discovery import build
from flask import jsonify
from datetime import datetime
from google.oauth2.credentials import Credentials

'''
when we are able to get credentials from the front end this code will automatically run when the app starts.


This file requires test credentials named test_creds.json in this format, in the same folder, 
{
    "provider": "gmail",
    "token": {
        "refresh_token": "????????",
        "client_id": "?????????",
        "client_secret": "?????????"
    }
}
'''

with open('test_creds.json') as json_file:
    raw_creds = json.load(json_file)

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

def construct_creds(info):
    """ Builds credentials from token info """

    creds = Credentials.from_authorized_user_info(info)
    return creds

creds = construct_creds(raw_creds['token'])

def test_user_emails():
    '''proves the the object retrieved with this function meets expected dimensions'''
    message_list = user_emails(creds)
    assert len(message_list['messages']) == 100
    assert len(message_list) == 3

def test_recent_id():
    '''proves the id retrieved with recent_id funtion is as expected'''
    message_list = user_emails(creds)
    recent = recent_id(message_list)
    assert len(recent) == 16