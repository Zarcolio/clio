#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from termcolor import colored

sStandardInput = ""

for x in sys.stdin:
    sStandardInput = sStandardInput + x 

#print (sStandardInput)

json_data = json.loads(sStandardInput)

#print (json_data["urls"])
for sUrl in json_data["urls"]:
    print (colored("URL = " + sUrl,"green"))

for app in json_data["applications"]:
    if app["version"]:
        sVersion = " " + str(app["version"])
    else:
        sVersion = ""
    print (str(app["name"]) + sVersion + " (" + app["confidence"] + "%) - " + app["website"])
