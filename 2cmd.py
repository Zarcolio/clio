#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import signal
import os

def signal_handler(sig, frame):
        print("\nCtrl-C detected, exiting...\n")
        sys.exit(0)


def FileNameSan(sFileName):
    sFileName = sFileName.replace("://", "-")
    sFileName = sFileName.replace(":", "-")
    sFileName = sFileName.replace("/", "-")
    return sFileName

signal.signal(signal.SIGINT, signal_handler)

# Get some commandline arguments:
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cmd", help="File containing one or more commands that should be executed. Use $2cmd$ or $2cmdsan$ in lowercase in each command line. $2cmd$ is replaced with each line from input. Use $cmdsan$ to sanitize a string for use in a filename.")
args = parser.parse_args()

if args.cmd:
    sCmdFile = args.cmd
else:
    parser.print_help(sys.stderr)
    sys.exit(1)
    
try:
    f = open(os.path.abspath(sCmdFile), 'r')
    aCmds = f.readlines()
    f.close()
except FileNotFoundError:
    print ("File not found, exiting...")
    sys.exit(1)
    
for strInput in sys.stdin:
    for sCmd in aCmds:
        sCmd = sCmd.strip()
        strInputSan = FileNameSan(strInput)
        sCmd = sCmd.replace("$2cmdsan$", strInputSan, len(sCmd))
        #sCmd = sCmd.strip()
        sCmd = sCmd.replace("$2cmd$", strInput, len(sCmd))
        #sCmd = sCmd.strip()
        sCmd = sCmd.replace("\n", "", len(sCmd))
        #print (sCmd)
        os.system(sCmd)