#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from tldextract import extract
import signal

def signal_handler(sig, frame):
        print("\nCtrl-C detected, exiting...\n")
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#logging.basicConfig()


for sInFqdn in sys.stdin:
    tsd, td, ts = extract(sInFqdn)
    sys.stdout.write (td + "\n")

sys.stdout.write ("\n")
