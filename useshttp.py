#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
import argparse
import re
import requests

def fHttpTest(sProtocol, sInFqdn, sPort, aStatus, sTimeout):
    if (sProtocol == "http" and sPort == "80") or (sProtocol == "https" and sPort == "443"):
        sHttpUrl = sProtocol + "://" + sInFqdn
    else:
        sHttpUrl = sProtocol + "://" + sInFqdn + ":" + sPort
        
    try:
        rHttp = requests.get(sHttpUrl, timeout=int(sTimeout))
        if args.status is None:
            sys.stdout.write (sHttpUrl + "\n")
            return True
        else:
            for sStatus in aStatus:
                sStatus = sStatus.lower()
                if re.match(r"^[1-5][0-9][0-9]$", sStatus):
                    if str(rHttp.status_code) == sStatus:
                        sys.stdout.write (sHttpUrl + "\n")
                elif sStatus == "info" or sStatus == "success" or sStatus == "redirect" or sStatus == "client-error" or sStatus == "server-error":
                    #print ("test")
                    iHttpStatus = int(rHttp.status_code)
                    if sStatus == "info" and iHttpStatus >= 100 and iHttpStatus <200:
                        sys.stdout.write (sHttpUrl + "\n")
                    if sStatus == "success" and iHttpStatus >= 200 and iHttpStatus <300:
                        sys.stdout.write (sHttpUrl + "\n")
                    if sStatus == "redirect" and iHttpStatus >= 300 and iHttpStatus <400:
                        sys.stdout.write (sHttpUrl + "\n")
                    if sStatus == "client-error" and iHttpStatus >= 400 and iHttpStatus <500:
                        sys.stdout.write (sHttpUrl + "\n")
                    if sStatus == "server-error" and iHttpStatus >= 500 and iHttpStatus <600:
                        sys.stdout.write (sHttpUrl + "\n")
                    return True
                else:
                    print ("Invalid HTTP status code(s)")
                    sys.exit()
    except requests.exceptions.RequestException:
        pass
 
def signal_handler(sig, frame):
	print("\nCtrl-C detected, quitting...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--ports", help="List of ports, separated by commas. Don't use spaces.")
parser.add_argument("-s", "--status", help="List of HTTP status codes or classes: info, success, client-error or server-error, separated by commas. Status codes and classes may be combined. Don't use spaces.")
parser.add_argument("-t", "--timeout", help="Time-out of the GET request in seconds.")
parser.add_argument("-x", "--https", help="Use only HTTP or HTTP, not both.")
args = parser.parse_args()


if args.ports is None:
    sPortArg = "443,80"
else:
    sPortArg = args.ports

if args.timeout is None:
    sTimeoutArg = "1"
else:
    sTimeoutArg = args.timeout

aPorts = sPortArg.split(",")

if args.status is not None:
    aStatus = args.status.split(",")
else:
    aStatus = []

if args.https:
	sHttps = args.https.lower()
else:
	sHttps = None

for sInFqdn in sys.stdin:
    sInFqdn = sInFqdn.strip()
    for sPort in aPorts:
        if (sHttps == "https") or (sHttps is None): 
        	fHttpTest("https", sInFqdn, sPort, aStatus, sTimeoutArg)
        if (sHttps == "http") or (sHttps is None): 
        	fHttpTest("http", sInFqdn, sPort, aStatus, sTimeoutArg)
        if (sHttps != "http") and (sHttps != "https") and (sHttps is not None):
        	print("Invalid protocol specification...")
        	sys.exit(1) 

   