#!/usr/bin/env python3
import os
import subprocess
import json
import pprint
import sys
import datetime

dir = "/etc/fastd/freifunk-saar/peers/"
nodeDataPath = "/var/www/nodes/nodes.json"
statePath = "/usr/bin/bat2nodes/state.json"

with open(nodeDataPath) as node_file:
	nodeData = json.load(node_file)

with open(statePath) as state_file:
	stateData = json.load(state_file)

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(nodeData)

i = 1
for f in os.listdir(dir):
	path = dir + f
	if os.path.isfile(path):
		file = open(path, 'r')
                keyline = ""
                nameline = ""

		for line in file:
			try:
				utf8line = line.decode("utf-8")
			except:
				print "error in utf8 decode -> " + line
				pass
			if "key" in utf8line:
				keyline = utf8line
			if ":" in utf8line:
				nameline = utf8line
		found = False
		offline = False
		lastseen = ""
			
		#print "Name : " + nameline
		#print "Key : " + keyline

		for n in nodeData["nodes"]:
			if n["name"] in nameline:
				found = True
				if n["flags"]["online"] != True:
					offline = True
					for s in stateData:
						if s["id"] == n["id"]:
							lastseen = s["lastseen"]
				break

		if found == False:
			print "ToDo " + str(i) + ":"
			i += 1
			print nameline + keyline
		if offline == True:
			print "ToDo " + str(i) + " (offline):"
			print nameline + " lastseen: " + str(datetime.datetime.fromtimestamp(lastseen)) 
			i += 1

