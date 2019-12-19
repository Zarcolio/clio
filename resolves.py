#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import signal
import argparse

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
	print ("Success: " + args.success)
	fSuccess = open(args.success, 'w')

if args.failed:
	print ("Failed: " + args.failed)
	fFailed = open(args.failed, 'w')


for strInput in sys.stdin:
	strInput = strInput.strip()
	try:
		result = socket.gethostbyname_ex(strInput)
		sys.stdout.write(strInput + "\n")
		if args.success:
			dIpAddresses = GetIpAddress(strInput)
			for sIpAddress in dIpAddresses: 
				fSuccess.write(strInput + ";" + sIpAddress + " \n")
	except socket.gaierror:
		if args.failed:
			fFailed.write(strInput + "\n")
		else:
			pass