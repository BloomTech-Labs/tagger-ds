from datetime import datetime
from google.oauth2.credentials import Credentials


def posix_datetime(utc_timestamp):
    """ Take a UTC Timestamp and return the POSIX datetime tuple """
    posix_date = datetime.utcfromtimestamp(utc_timestamp)
    return posix_date

def load_user_token(token):
    """ Loads user token """

    user_token = json.loads(token)
    return user_token

def construct_creds(info):
    """ Builds credentials from token info """
    creds = Credentials.from_authorized_user_info(info)
    return creds
