#!/usr/bin/env python3

import cgi,os
import requests
import datetime
import subprocess
import json
timestamp = str( datetime.datetime.today())
timestamp = timestamp.replace(":", ".")

from picamera import PiCamera
from time import sleep

# enable debugging
import cgitb
cgitb.enable()


araPostError=""
faceExist = 0
form = cgi.FieldStorage()
action = form.getvalue('action')
action = str(action)
#action = "send"
flog = open("/home/pi/Lottery/log.txt", 'a')
flog.write(timestamp + " action = " + action + "\n")
print ("Content-type: text/html\n\n")
myResponseName = ""
if action == "send":
	#print ("<body><h1>Automic Lottery cgi Response</h1>")
	#print ("action: " + action + "<br><br>")
	if os.path.isfile("/home/pi/Lottery/face.jpg"):
		faceExist = 1
		flog.write(timestamp + " face.jpg exist \n")
		url = "http://automic_server/ara/api/data/v1/packages"
		data = {
		"name": timestamp,
		"status": "Active",
		"folder": {
		"name": "LOTTERY"
		},
		"owner": {
		"type": "User",
		"name": "100/ARA/ARA"
		},
		"custom_type": {
		"name": "Lottery"
		},
		"dynamic": {},
		"application": {
		"name": "Lottery"
		}}
		try:
			myResponse = requests.post(url,auth=('100/ara/ara', 'ara'),json=data)
			data = json.dumps(myResponse.json())
			myResponseName = json.loads(data)

			f = open("/home/pi/Lottery/status.txt", 'w')
			f.write('ARA package created')
			f.close
			flog.write(timestamp + " Package created: " + myResponseName["name"] + "\n")
		except Exception as e:
			flog.write(timestamp + " Error posting to ARA\n" + str(e)+"\n")
			araPostError="<p>Error: " + str(e) + "</p>" 

	else:
		f = open("/home/pi/Lottery/status.txt", 'w')
		f.write('no picture found')
		f.close
		flog.write(timestamp + " face.jpg no exist. No Package created \n")
elif action == "takePicture":
	try:
		camera = PiCamera()
		camera.video_stabilization = True
		camera.resolution = 'XGA'
		camera.annotate_text = timestamp
		camera.capture('/home/pi/Lottery/face.jpg')
		flog.write(timestamp + " Created picture /home/pi/Lottery/face.jpg \n") 
	except Exception as e:
		flog.write(timestamp + " Error take picture\n" + str(e)+"\n")


result = subprocess.check_output(["cat", "/var/www/html/index.html1"], universal_newlines=True)
print (result)

#server  = str(os.environ.get('SERVER_ADDR'))
#print ("<p><a href=\"http://" +  server + "\">Back</a></p>")
if action == "send":
	if myResponseName != "":
		print ("<br><p>ARA pkg:<br/>" + myResponseName["name"] + "</p>")
	elif faceExist == 0:
		 print ("<br><p>No picture<br/>Take a new.</p>")
if araPostError != "":
	print (araPostError)
result = subprocess.check_output(["cat", "/var/www/html/index.html2"], universal_newlines=True)
print (result)

#print ("</body>")
flog.close
