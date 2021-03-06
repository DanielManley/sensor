#Create sensor that uses orange pi zero and relay to sense voltage
#!/usr/bin/env python

import os
import sys

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

#import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import time

from pyA20.gpio import gpio
from pyA20.gpio import connector
from pyA20.gpio import port

#client = mqtt.Client()
#client.connect("mqtt.thingspeak.com",1883,60)
channelId = "1112212"  # Put your channel ID here
apiKey = "AZP2G6XY3CKLAYFC"  # Put the API write key here

starttime = time.time()
GVEA = port.PA12 #set pin 12 to GVEA
gpio.init() #initiate GPIO usage
gpio.setcfg(GVEA,gpio.INPUT) #set GVEA to input
print ("VoltageSensor is running.")
laststate = 2
try:
    print ("Press CTRL+C to exit")
    while True:
        state = gpio.input(GVEA)      # Read button state
        if state != laststate:
		print ("the state is " + str(state))
		text2= "field1=" + str(state)
		publish.single("channels/%s/publish/%s" % (channelId,apiKey), text2, hostname = "mqtt.thingspeak.com")
		#client.publish("channels/%s/publish/%s" % (channelId,apiKey),text2)
	laststate = state
#	time.sleep(0.05)
	if ((int(time.time() - starttime) % 1200.0 )==0):
		text2= "field1=" + str(state)
		publish.single("channels/%s/publish/%s" % (channelId,apiKey), text2, hostname = "mqtt.thingspeak.com")
		print ("periodic update complete" + str (state) +" " + str(time.time()))
		time.sleep(2)
except KeyboardInterrupt:
	print ("Goodbye.")
