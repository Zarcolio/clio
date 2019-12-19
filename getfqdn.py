#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import urllib.parse
import argparse
import signal

def signal_handler(sig, frame):
        print("\nCtrl-C detected, exiting...\n")
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

aTld = []

# Get some commandline arguments:
sArgParser=argparse.ArgumentParser()
sArgParser.add_argument('--tlds', help='Enter alternative file with TLDs.')
aArguments=sArgParser.parse_args()

if aArguments.tlds:
    fTlds = aArguments.tlds
else:
    fTlds = sys.path[0] + "/tlds.txt"
    

# RFC compliant FQDN, regex by https://github.com/guyhughes/fqdn:
strRegex = r'((?!-)[-A-Z\d]{1,62}(?<!-)\.)+[A-Z]{1,62}'

# Read all TLDs from file:
try:
    f = open(fTlds, 'r')
    aTld = f.readlines()
    f.close()
except FileNotFoundError:
    print("File with TLDs named " + fTlds + " was not found.")
    sys.exit(2)

#Read from standard input:
for strInput in sys.stdin:
    # Some URLs have double encoded values, so 2 times "unquote":
    strInput = urllib.parse.unquote(strInput)
    strInput = urllib.parse.unquote(strInput)
    
    # Validate the FQDN based on regex:
    matches = re.finditer(strRegex, strInput, re.IGNORECASE)

    # Validate by TLD:
    for matchNum, match in enumerate(matches, start=1):
        match = "{match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group())
        for sTld in aTld:
            sTld = sTld.strip()
            if sTld:
                if sTld[0] != "#":
                    if match.endswith("." + sTld):
                        sys.stdout.write (match.lower())
            else:
                print ("Invalid TLD file.")

        sys.stdout.write ("\n")
