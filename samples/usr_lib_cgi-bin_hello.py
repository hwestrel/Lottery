#!/usr/bin/env python3

import cgi,os
import requests
import datetime
timestamp = str( datetime.datetime.today())
timestamp = timestamp.replace(":", ".")

print ("Content-type: text/html\n\n")
print ("<body><h1>Automic Lottery cgi Response</h1>")

form = cgi.FieldStorage()
action = form.getvalue('action')

print ("action: " + action + "<br><br>")

if action == "cancel":
	print ("Picture removed, please create a new, or not...")
elif action == "send":
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
	myResponse = requests.post(url,auth=('100/ara/ara', 'ara'),json=data)
	
	print ("ARA contacted, ARA will fetch the picture, ") 

 
server  = str(os.environ.get('SERVER_ADDR'))
print ("<p><a href=\"http://" +  server + "\">Back</a></p>") 

print ("<br><p>" + str(myResponse.json()) + "</p>")
print ("</body>")
