#!/usr/bin/env python3

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time, sys, speech_recognition

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1kBSJDmjRba7FHl_Y5KjrU7RE55wsCS9AJkZoBocIjUE'
SAMPLE_RANGE_NAME = 'A2'

def main():
    creds = None
    
    # token.pickle stores user access & refresh tokens
    # Created automatically on authorization flow completion.
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
            # creds = flow.run_local_server(port=0)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    values = [
        [
            time.time() / 60 / 60 / 24 + 25569 - 4 / 24,
            listen()
        ]
    ]
    body = { 'values' : values }
    result = sheet.values().append(
        spreadsheetId = SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
        valueInputOption = 'USER_ENTERED', body = body
    ).execute()
    print(result)

# Retrieve audio from a microphone and return a string represtending the speech
def listen():
    recognizer = speech_recognition.Recognizer()
    mic = speech_recognition.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print('Talk now!')
        audio = recognizer.listen(mic)
    response = ''
    try:
        response = recognizer.recognize_google(audio)
    except speech_recognition.RequestError:
        print('Speech Recognition API Unavailable!')
        return ''
    except speech_recognition.UnknownValueError:
        print('Unable to recognize speech!')
        return ''
    except OSError as e:
        print(e.args)
    except:
        print('Unknown error occurred: ', sys.exc_info()[0])
        return ''
    return response

if __name__ == '__main__':
    main()
