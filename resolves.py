#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import signal
import argparse
import dns.resolver
from random import choice
from string import ascii_letters, digits


def signal_handler(sig, frame):
	sys.stderr.write("\nCtrl-C detected, quitting...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

def GetIpAddress(sHostName):
    try:
        aResults = socket.getaddrinfo(sHostName, 0)
    except:
        return False
    
    dResolved = {}
    for sIpAddress in aResults:
        sIpAddress = sIpAddress[4][0]
        dResolved [sIpAddress] = sIpAddress
    return dResolved

def GetCname(sHostName):
    try:
        aResults = dns.resolver.query(sHostName, 'CNAME')
    except:
        return False
    
    dResolved = {}
    for sCname in aResults:
        Cname = str(sCname.target)
        dResolved [Cname] = Cname
    return dResolved

parser = argparse.ArgumentParser()
parser.add_argument("-nc", "--nocname", help="Ommit FQDN from printing to the screen or saving it to the plain file when it points to a CNAME record. It will be saved to the CSV file if requested.", action="store_true")
parser.add_argument("-os", "--success", help="Define an output CSV file for succesfully resolved FQDNs. This file will contain the hostnames found with their corresponding IP addresses.")
parser.add_argument("-of", "--failed", help="Define an output file for FQDNs that failed to resolve.")
parser.add_argument("-op", "--plain", help="Define an output file for succesfully resolved FQDNs. This file will contain only hostnames found.")

args = parser.parse_args()

if args.plain:
	fPlain = open(args.plain, 'w')

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

    dIpAddressesRandom = GetIpAddress(sWildcardFqdn)
    
    #print(strInput)
    dIpAddresses = GetIpAddress(str(strInput))
    dCnames = GetCname(str(strInput))
    
    #for sIpAddressRandom in dIpAddresses:
    if dIpAddressesRandom:
        #print ("Wildcard: "+strInput + ":" +str(dIpAddressesRandom))
        if not str(dIpAddressesRandom) in dRembemberdIpAddressesRandom:
            sys.stdout.write(strInput + "\n")
            if args.plain:
                fPlain.write(strInput + " \n")
        dRembemberdIpAddressesRandom[str(dIpAddressesRandom)]=True
        #print (dIpAddressesRandom)
        #if sIpAddressRandom in dIpAddresses:
        #    print ("Wildcard detected:" + sIpAddressRandom + " for " + strInput)
    else:
        if not dCnames or not args.nocname:
            sys.stdout.write(strInput + "\n")
            if args.plain:
                fPlain.write(strInput + " \n")

        #print(str(dIpAddresses))
    
    if args.success:
        if dCnames:
            for sCname in dCnames: 
                #fSuccess.write(strInput + ";" + sIpAddress + " \n")
                fSuccess.write(strInput + ";" + sCname[:-1] + " \n")
        else:
            if dIpAddresses:
                for sIpAddress in dIpAddresses: 
                    fSuccess.write(strInput + ";" + sIpAddress + " \n")
                
    
