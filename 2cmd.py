#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import signal
import os
from termcolor import colored

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
parser = argparse.ArgumentParser(description="This script takes input lines from stdin and inserts them in the commands provided in the commands file. This way you can execute a certain command many times. For example you can take screen shots of URLs with cutycapt provided by output of another command.")
parser.add_argument("cmd", help="File containing one or more commands that should be executed. Use $2cmd$ or $2cmdsan$ in lowercase in each command line. $2cmd$ is replaced with each line from input. Use $cmdsan$ to sanitize a string for use in a filename.")
parser.add_argument("-v", "--verbose", help="In red, show the commands that are created from stdin and the provide config file.", action="store_true")
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
        if not strInput.strip():
            continue
        
        strInputSan = FileNameSan(strInput)
        sCmd = sCmd.replace("$2cmdsan$", strInputSan, len(sCmd))
        #sCmd = sCmd.strip()
        sCmd = sCmd.replace("$2cmd$", strInput, len(sCmd))
        #sCmd = sCmd.strip()
        sCmd = sCmd.replace("\n", "", len(sCmd))
        if args.verbose:
            sys.stderr.write((colored(sCmd,"green"))+"\n")
        os.system(sCmd)