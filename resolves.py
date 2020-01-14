#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import signal
import argparse
from random import choice
from string import ascii_letters, digits

def signal_handler(sig, frame):
	print("\nCtrl-C detected, quitting...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

def GetIpAddress(sHostName):
	aResults = socket.getaddrinfo(sHostName, 0)
	dResolved = {}
	for sIpAddress in aResults:
		sIpAddress = sIpAddress[4][0]
		dResolved [sIpAddress] = sIpAddress

	return dResolved

parser = argparse.ArgumentParser()
parser.add_argument("-oS", "--success", help="Define an output CSV file for succesfully resolved FQDNs. This file will contain the hostnames found with their corresponding IP addresses.")
parser.add_argument("-oF", "--failed", help="Define an output file for FQDNs that failed to resolve.")
args = parser.parse_args()

if args.success:
	fSuccess = open(args.success, 'w')

if args.failed:
	fFailed = open(args.failed, 'w')

sRandom =  ''.join([choice(ascii_letters + digits) for i in range(20)])
dRembemberdIpAddressesRandom = {}

for strInput in sys.stdin:
    strInput = strInput.strip()
    sWildcardFqdn = sRandom + "." + strInput
    #print(sWildcardFqdn)

    try:
        dIpAddressesRandom = GetIpAddress(sWildcardFqdn)
    except:
        dIpAddressesRandom = False
    
    try:
        dIpAddresses = GetIpAddress(strInput)
        #for sIpAddressRandom in dIpAddresses:
        if dIpAddressesRandom:
            #print ("Wildcard: "+strInput + ":" +str(dIpAddressesRandom))
            if not str(dIpAddressesRandom) in dRembemberdIpAddressesRandom:
                sys.stdout.write(strInput + "\n")
            dRembemberdIpAddressesRandom[str(dIpAddressesRandom)]=True
            #print (dIpAddressesRandom)
            #if sIpAddressRandom in dIpAddresses:
            #    print ("Wildcard detected:" + sIpAddressRandom + " for " + strInput)
        else:    
            sys.stdout.write(strInput + "\n")
            #print(str(dIpAddresses))
        
        if args.success:
            for sIpAddress in dIpAddresses: 
                fSuccess.write(strInput + ";" + sIpAddress + " \n")
    except socket.gaierror:
        if args.failed:
            fFailed.write(strInput + "\n")
        else:
            pass
    #except:
    #    print ("Other error")
    #    pass
    