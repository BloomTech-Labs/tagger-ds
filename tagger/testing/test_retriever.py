from __future__ import print_function
import pickle
import os.path
import base64
from bs4 import BeautifulSoup
import bleach
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pytest


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # In production this authorization method will be handled through a JSON
    # retrieved from the BE server.
if os.path.exists('token.pickle'):
  with open('token.pickle', 'rb') as token:
    creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
  if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
  else:
    flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
  with open('token.pickle', 'wb') as token:
    pickle.dump(creds, token)
    
# Build the Google Service
service = build('gmail', 'v1', credentials=creds)

# Call the Gmail API
message = service.users().messages().list(userId='me').execute()

# Find most recent message
recent_msg_id = message['messages'][0]['id']
    
# Recent message list/this will be important when tracking 
# which emails have been retrieved versus those that haven't.
recent_msg_list = message['messages']

# Call message content
message_content = service.users().messages().get(
    userId='me', id=recent_msg_id).execute()

# Call message body
message_body = message_content['payload']['parts']
message_body_dict = dict(message_body[0])

# Decode base64 encoding
decode = message_body_dict['body']['data']
decodedContents = base64.urlsafe_b64decode(decode.encode('ASCII'))

# Clean the text
text = BeautifulSoup(decodedContents, 'html.parser')
text = str(text.text)
text = re.sub(r"http\S+", "", text)

# Output
#print("Recent Message: ", recent_msg_id, "\n\nRecent Message List: ", recent_msg_list, "\n\nMessage Body: ", text)



def generate_message():

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # In production this authorization method will be handled through a JSON
    # retrieved from the BE server.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Build the Google Service
    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    message = service.users().messages().list(userId='me').execute()

    message_count = len(message['messages'])

    return message_count

def generate_message_body():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # In production this authorization method will be handled through a JSON
    # retrieved from the BE server.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    
    # Build the Google Service
    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    message = service.users().messages().list(userId='me').execute()

    # Find most recent message
    recent_msg_id = message['messages'][0]['id']
    
    # Recent message list/this will be important when tracking 
    # which emails have been retrieved versus those that haven't.
    recent_msg_list = message['messages']

    # Call message content
    message_content = service.users().messages().get(
    userId='me', id=recent_msg_id).execute()

    # Call message body
    message_body = message_content['payload']['parts']
    message_body_dict = dict(message_body[0])

    # Decode base64 encoding
    decode = message_body_dict['body']['data']
    decodedContents = base64.urlsafe_b64decode(decode.encode('ASCII'))

    # Clean the text
    text = BeautifulSoup(decodedContents, 'html.parser')
    text = str(text.text)
    text = re.sub(r"http\S+", "", text)

    # Output
    return (recent_msg_id, recent_msg_list, text)

def test_gmail_api():
    message_count = generate_message()
    assert message_count == 100, 'test gmail api'

def test_gmail_content():
    pack = generate_message_body()
    recent_msg_id = pack[0]
    recent_msg_list = pack[1]
    text = pack[2]
    assert type(recent_msg_id) == type("String")
    assert len(recent_msg_list) == 100
    assert type(text) == type("String")


    #print("Recent Message: ", recent_msg_id, "\n\nRecent Message List: ", recent_msg_list, "\n\nMessage Body: ", text) 

