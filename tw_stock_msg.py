#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys

def showCopyRight():
    print ("")
    print ("TWSE Stock Info Version 0.1 (C)Copyright Hsu Chih-Ming")
    print ("")

def showHelpMsg():
    print ("Usage: ")
    print ("  python3 " + sys.argv[0] + " -d -u -s <STOCK CODE> -i <STOCK CODE>")
    print ("")
    print ("Arguments:")
    print ("")
    print ("  -d: Turn on DEBUG info")
    print ("  -u: Update all stock code")
    print ("  -s <STOCK CODE>: Update the record of stock code.")
    print ("  -i <STOCK CODE>: Show information of stock code.")

    