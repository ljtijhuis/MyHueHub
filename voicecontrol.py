#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from pynetgear import Netgear
from phue import Bridge

def setLights(lights, setOn):
	for light in lights:
		light.on = setOn
		
hueMac = 'MAC_HUE_BRIDGE'
BING_KEY = "BING_API_KEY" # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings

netgear = Netgear('password')

hueIp = -1

print 'Connecting to router. Devices found:'
for device in netgear.get_attached_devices():
	print device
	if device.mac == hueMac:
		hueIp = device.ip

if hueIp == -1:
	print 'Hue not found, aborting..'
	exit
else:
	print 'Hue found at ' + hueIp

print 'Connecting to Hue'

b = Bridge(hueIp)

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

print 'Connected! Available lights:'
for l in b.lights:
    print(l.name)

# obtain audio from the microphone
r = sr.Recognizer()

print 'Polling for commands to control lights..'

while True:

    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        
    # recognize speech using Microsoft Bing Voice Recognition
    try:
        print("Recognizing voice..")
        voiceCmd = r.recognize_bing(audio, key=BING_KEY) #recognize_sphinx(audio)
        print("Microsoft Bing Voice Recognition thinks you said " + voiceCmd)
    
        if 'lights' in voiceCmd and 'on' in voiceCmd:
            print 'On command heard, turn ON the lights!'
            setLights(b.lights, True)
        elif 'lights' in voiceCmd and 'off' in voiceCmd:
            print 'Off command heard, turn OFF the lights!'
            setLights(b.lights, False)
        
    
    except sr.UnknownValueError:
        print("Microsoft Bing Voice Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
    
	time.sleep(5)