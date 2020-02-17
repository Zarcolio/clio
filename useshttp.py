#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
import argparse
import re
import requests

def signal_handler(sig, frame):
    sys.stderr.write("\nCtrl-C detected, quitting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

requests.packages.urllib3.disable_warnings() 

def fHttpTest(sProtocol, sInFqdn, sPort, aStatus, sTimeout):
    if (sProtocol == "http" and sPort == "80") or (sProtocol == "https" and sPort == "443"):
        sHttpUrl = sProtocol + "://" + sInFqdn
    else:
        if (sProtocol == "http" and sPort == "443"):
            return False
        else:
            sHttpUrl = sProtocol + "://" + sInFqdn + ":" + sPort
        
    try:
        rHttp = requests.get(sHttpUrl, timeout=int(sTimeout), verify=False)
        if args.status is None:
            if args.slash:
                sHttpUrl += "/"
            sys.stdout.write (sHttpUrl + "\n")
            if args.csv:
                fCsv.write(sHttpUrl + " ;" + str(rHttp.status_code) +"\n")
            return True
        else:
            for sStatus in aStatus:
                sStatus = sStatus.lower()
                if re.match(r"^[1-5][0-9][0-9]$", sStatus):
                    if str(rHttp.status_code) == sStatus:
                        if args.slash:
                            sHttpUrl += "/"
                        sys.stdout.write (sHttpUrl + "\n")
                        if args.csv:
                            fCsv.write(sHttpUrl + " ;" + str(rHttp.status_code) +"\n")
                        return True
                elif sStatus == "info" or sStatus == "success" or sStatus == "redirect" or sStatus == "client-error" or sStatus == "server-error":
                    if args.slash:
                        sHttpUrl += "/"
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
                    if args.csv:
                        fCsv.write(sHttpUrl + ";" + str(rHttp.status_code) +"\n")

                    return True
                else:
                    sys.stderr.write ("Invalid HTTP status code(s)")
                    sys.exit()
    except requests.exceptions.RequestException:
        pass
 
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--ports", help="List of ports, separated by commas. Don't use spaces.")
parser.add_argument("-s", "--status", help="List of HTTP status codes or classes: info, success, client-error or server-error, separated by commas. Status codes and classes may be combined. Don't use spaces.")
parser.add_argument("-t", "--timeout", help="Time-out of the GET request in seconds.")
parser.add_argument("-x", "--httpx", help="Use either HTTP or HTTP, not both.")
parser.add_argument("-1", "--one", help="If HTTPS found, don't try HTTP for the same port.", action="store_true", default=False)
parser.add_argument("-c", "--csv", help="Export to CSV file.")
parser.add_argument("-l", "--slash", help="Add trailing slash.", action="store_true")
args = parser.parse_args()

if args.csv:
	fCsv = open(args.csv, 'w', buffering=1)

if args.ports:
    sPortArg = args.ports
else:
    sPortArg = "443,80"

if args.timeout:
    sTimeoutArg = args.timeout
else:
    sTimeoutArg = "1"

aPorts = sPortArg.split(",")

if args.status:
    aStatus = args.status.split(",")
else:
    aStatus = []

if args.httpx:
	sHttpx = args.httpx.lower()
else:
	sHttpx = None

for sInFqdn in sys.stdin:
    sInFqdn = sInFqdn.strip()
    for sPort in aPorts:
        if (sHttpx == "https" and sPort != "80") or (sHttpx is None and sPort != "80"): 
            bHttpTestResult = fHttpTest("https", sInFqdn, sPort, aStatus, sTimeoutArg)
        if not bHttpTestResult or not args.one:
            if (sHttpx == "http" and sPort != "443") or (sHttpx is None and sPort != "443"): 
                fHttpTest("http", sInFqdn, sPort, aStatus, sTimeoutArg)
        if (sHttpx != "http") and (sHttpx != "https") and (sHttpx is not None):
            sys.stderr.write("Invalid protocol specification...")
            sys.exit(1) 

   
