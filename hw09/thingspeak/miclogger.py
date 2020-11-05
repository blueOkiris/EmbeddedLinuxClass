#!/usr/bin/env python3
# Reads a TMP101 sensor and posts its temp on ThinkSpeak
# https://thingspeak.com/channels/538706
# source setup.sh to set THING_KEY

import requests
import os, sys
import time
import speech_recognition

# Retrieve audio from a microphone and return a string represtending the speech
def listen():
    recognizer = speech_recognition.Recognizer()
    mic = None
    for i, micName in enumerate(speech_recognition.Microphone.list_microphone_names()):
        if micName.startswith('Logitech USB Microphone'):
            mic = speech_recognition.Microphone(device_index = i)
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print('Talk now!')
        audio = recognizer.listen(mic)
    response = ''
    try:
        response = recognizer.recognize_google(audio)
    except speech_recognition.RequestError:
        print('Speech Recognition API Unavailable!')
        return '~Api unavailable'
    except speech_recognition.UnknownValueError:
        print('Unable to recognize speech!')
        return '~No speech Recognized'
    except OSError as e:
        print(e.args)
    except:
        print('Unknown error occurred: ', sys.exc_info()[0])
        return '~Unknown error'
    return response

# Get the key (See setup.sh)
key = os.getenv('THING_KEY', default="")
if(key == ""):
    print("THING_KEY is not set")
    sys.exit()

url = 'https://api.thingspeak.com/update'
print(url)

while(1):
    speech = listen()
    print('You said: ' + speech)
        
    payload = dict(api_key = key, field1 = speech)
    r = requests.get(url, stream = True, data = payload)
    print(r)
    print(r.text)

    time.sleep(1*60)
