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

#TMP101a='/sys/class/i2c-adapter/i2c-2/2-0048/hwmon/hwmon0/'
#TMP101b='/sys/class/i2c-adapter/i2c-2/2-0049/hwmon/hwmon1/'

# Get the key (See setup.sh)
key = os.getenv('THING_KEY', default="")
if(key == ""):
    print("THING_KEY is not set")
    sys.exit()

url = 'https://api.thingspeak.com/update'
print(url)

while(1):
    #f = open(TMP101a+'temp1_input', "r")
    #temp1=f.read()[:-1]     # Remove trailing new line
    # Convert from mC to C
    #temp1 = int(temp1)/1000
    #f.close()
    #print("temp1: " + str(temp1))

    #f = open(TMP101b+'temp1_input', "r")
    #temp2=f.read()[:-1]
    #temp2 = int(temp2)/1000
    #f.close()
    #print("temp2: " + str(temp2))
    
    # Get speech input
    speech = listen()
    print('You said: ' + speech)
        
    payload = dict(api_key = key, field1 = speech)
    r = requests.get(url, stream = True, data = payload)
    print(r)
    print(r.text)

    time.sleep(15*60)
