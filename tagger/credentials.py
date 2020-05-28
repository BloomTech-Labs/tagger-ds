from datetime import datetime
import json
from google.oauth2.credentials import Credentials

def construct_creds(info):
    """ Builds credentials from token info """

    creds = Credentials.from_authorized_user_info(info)
    return creds
