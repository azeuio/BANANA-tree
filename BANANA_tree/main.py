#!/usr/bin/env python3
from sys import argv
import subprocess
from custom_exit import exit
from exit_codes import *
import tempfile
from checker_manager import CheckerManager

def print_help():
    with tempfile.TemporaryFile("w") as f:
        if subprocess.call(["man", "BANANA-tree"], stderr=f):
            exit(EXIT_MAN_PAGE_NOT_FOUND)

if __name__ == '__main__':
    if ("-h" in argv) or ("--help" in argv):
        print_help()
    manager = CheckerManager(argv)
    if manager.check():
        exit(EXIT_INVALID_PATH, manager.path)
    exit(EXIT_OK)