#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from tldextract import extract
import signal
import argparse

def signal_handler(sig, frame):
    sys.stderr.write("\nCtrl-C detected, quitting...\n")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser()
parser.add_argument("format", help="Each number from 1 to 9 is replaced with the corresponding domain level taken from the input (takes vTLD such as co.uk into account). For example, if the argument 3.2.1 is given and stdin supplies sub5.sub4.sub3.example.co.uk then sub3.example.co.uk is returned. The dots are free-form, any character can be used.")
parser.add_argument("-321", "--extract321", help="Separeate second (2) and top level domain (1), and the remaining part (3).", action="store_true")
args = parser.parse_args()

'''
This script can be used for example when searching for amazon buckets. Use: 
    cat domainlist.txt|splitxld.py 2.1>buckets.txt
    cat domainlist.txt|splitxld.py 2-1>>buckets.txt
    cat domainlist.txt|splitxld.py 2>>buckets.txt"
'''

for sInFqdn in sys.stdin:
    if not sInFqdn.strip():
        continue
    
    sOutput = args.format
    # Because of vTLD suffixes:
    dl3, dl2, dl1 = extract(sInFqdn)
    if args.extract321:
            sOutput = sOutput.replace("1",dl1)
            sOutput = sOutput.replace("2",dl2)
            sOutput = sOutput.replace("3",dl3)
    else:
            sInFqdn = sInFqdn.rsplit(dl1, 1)[0]
            sOutput = sOutput.replace("1",dl1)
            aFqdnSplit = sInFqdn.strip().split(".")
            
            i = len(aFqdnSplit)
            for sDomainLevel in aFqdnSplit:
                i -= 1
                if i > 9:
                    continue
                sOutput = sOutput.replace(str(i+1),sDomainLevel)
    
    sys.stdout.write(sOutput + "\n")
