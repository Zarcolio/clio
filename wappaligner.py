#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import urllib.parse
from termcolor import colored

sStandardInput = ""

for x in sys.stdin:
    sStandardInput = sStandardInput + x 

#print (sStandardInput)
try:
    json_data = json.loads(sStandardInput)
except:
    pass


for x in json_data["urls"]:
    print (x)
    
for sUrl in json_data["urls"]:
    print (colored("URL = " + sUrl,"green"))
#    print (colored("URL = " + sUrl["status"],"green"))

for app in json_data["applications"]:
    if app["version"]:
        sVersion1 = " " + str(app["version"])
        sVersion2 = " \"" + str(app["version"]) + "\""  
    else:
        sVersion1 = ""
        sVersion2 = ""

    sGoogleUrl = "https://www.google.com/search?q=" + urllib.parse.quote("\"" + app["name"] + "\"" + sVersion2 + " cve | exploit | vulnerability")
    print (app["name"] + sVersion1 + " (" + app["confidence"] + "%) - " + app["website"] + " - " + sGoogleUrl)
