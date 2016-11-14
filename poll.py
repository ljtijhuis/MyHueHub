import sys
import time, threading
from pynetgear import Netgear
from phue import Bridge

def setLights(lights, setOn):
	for light in lights:
		light.on = setOn

#if any of these are connected, keep lights on
presentDevices = ['MAC_1', 'MAC_2']
hueMac = 'MAC_HUE'

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

print 'Polling for devices to set lights..'

while True:
	connected = 0

	for device in netgear.get_attached_devices():
	   for mac in presentDevices:
		   if device.mac == mac:
			   connected = 1
			   break;

	if connected:
		print 'Devices are connected, turn ON the lights!'
		setLights(b.lights, True)
	else:
		print 'Devices disconnected, turn OFF the lights!'
		setLights(b.lights, False)
	time.sleep(5)

	
