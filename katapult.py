from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
from apiclient.http import MediaFileUpload
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# Populate the CLIENT_SECRET_FILE using non-sensitive data from auth.json
# and with sensitive data taken from environment variables
with open('auth.json', 'r') as auth:
    json_string = auth.read()
parsed_json = json.loads(json_string)
parsed_json['installed']['client_id'] = os.environ.get('KATAPULT_CLIENT_ID')
parsed_json['installed']['client_secret'] = os.environ.get('KATAPULT_CLIENT_SECRET')
secret_json_string = json.dumps(parsed_json, sort_keys=True, separators=(',',':'))
with open('secret.json', 'w') as secret:
    secret.write(secret_json_string)

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'katapult.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def insert(service,file,parent_id):
    """Uploads a file.

    """
    media = MediaFileUpload(file,resumable=True)
    file_metadata =  {'title':'Test text file'}
    if parent_id:
        file_metadata['parents'] = [{'id':parent_id}]
    try:
        file = service.files().insert(body=file_metadata,media_body=media).execute()
        return file
    except errors.HttpError, error:
        print('An error occurred: %s' % error)
        return None

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)

    uploaded_file = insert(service,'files/testupload.txt','0Byn7eiAVCHMNaGZaaGcybGYwdDA')
    if uploaded_file: print('Success: uploaded file %s' % uploaded_file.get('title'))

if __name__ == '__main__':
    main()
