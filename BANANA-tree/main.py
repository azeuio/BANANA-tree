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
    if (len(argv) == 1):
        path_to_check = "."
    else:
        path_to_check = argv[1]
    manager = CheckerManager()
    if manager.check(path_to_check) == False:
        exit(EXIT_INVALID_PATH)
    exit(EXIT_OK)