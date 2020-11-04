#!/usr/bin/env python3

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import time, sys, speech_recognition

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1kBSJDmjRba7FHl_Y5KjrU7RE55wsCS9AJkZoBocIjUE'
RANGE_NAME = 'A2'

def main():
    # Shows basic usage of the Sheets API and writes values to a spreadsheet.
    store = file.Storage('tokenPython.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http = creds.authorize(Http()))

    # Call the Sheets API && compute timestamp and pass the first two arguments
    values = [
        [
            time.time() / 60 / 60 / 24 + 25569 - 4 / 24,
            sys.argv[1], sys.argv[2]
        ]
    ]
    body = { 'values': values }
    result = service.spreadsheets().values().append(
        spreadsheetId = SPREADSHEET_ID, range = RANGE_NAME,
        
        #  How the input data should be interpreted.
        valueInputOption='USER_ENTERED',
        
        # How the input data should be inserted.
        # insertDataOption = 'INSERT_ROWS',
        
        body = body
    ).execute()
    
    updates = result.get('updates', [])
    # print(updates)

    if not updates:
        print('Not updated')

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
