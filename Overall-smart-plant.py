
import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import playsound

authenticator = IAMAuthenticator('UH_AiWIbt3uflaEMJGLbpJk6JIL3yJZ7_LHpXQpSaRNB')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url('https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/d8ab37c5-f3ff-4da8-9c91-fdc0430f7458')

with open('new.mp3', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            'Hello this your plant warm greetings to you',
            voice='en-US_AllisonV3Voice',
            accept='audio/mp3'
            ).get_result().content)

playsound.playsound('new.mp3')



#Provide your IBM Watson Device Credentials
organization = "roduhu"
deviceType = "iotdevice"
deviceId = "1001"
authMethod = "token"
authToken = "1234567890"


# Initialize the device client.
T=0
H=0
S=0
P=0
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])


        if cmd.data['command']=='motor on':
                print("MOTOR ON IS RECEIVED")
                
                
        elif cmd.data['command']=='motor off':
                print("MOTOR OFF IS RECEIVED")
        
        if cmd.command == "setInterval":
                if 'interval' not in cmd.data:
                        print("Error - command is missing required information: 'interval'")
                else:
                        interval = cmd.data['interval']
        elif cmd.command == "print":
                if 'message' not in cmd.data:
                        print("Error - command is missing required information: 'message'")
                else:
                        print(cmd.data['message'])

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        T=random.randint(27,40)
        H=random.randint(32,65)
        S=random.randint(20,95)
        #Send Temperature & Humidity to IBM Watson
        data = {"d":{ 'temperature' : T, 'humidity': H,'soilmoisture': S }}
        #print data
        def myOnPublishCallback():
           
            print ("Published Temperature = %s C" % T, "Humidity = %s %%" % H,"Soilmoisture = %s %%" % S,"to IBM Watson")
            if S<=50:
             print("MotorON")
            else:
             print("MotorOFF")

        success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(10)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
