#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import signal
from urllib.parse import unquote  
import argparse

def signal_handler(sig, frame):
    sys.stderr.write("\nCtrl-C detected, quitting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

# Get some commandline arguments:
sArgParser = argparse.ArgumentParser(description='URL decode a string from stdin x times')
sArgParser.add_argument("-c", '--count', help='Url decode x times.', default=1)
argument=sArgParser.parse_args()

for strInput in sys.stdin:
    for x in range(0, int(argument.count)):
        strInput = unquote(strInput)
       
    sys.stdout.write(strInput)