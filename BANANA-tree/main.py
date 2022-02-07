#!/usr/bin/env python3
from sys import argv
import subprocess
from custom_exit import exit
from exit_codes import *

def print_help():
    subprocess.call(["man", "BANANA-tree"])

if __name__ == '__main__':
    if len(argv) == 1:
        exit(EXIT_INVALID_NUMBER_OF_PARAMS)
    if ("-h" in argv) or ("--help" in argv):
        print_help()
    exit(EXIT_OK)