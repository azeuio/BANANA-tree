#!/usr/bin/env python3
import os
import sys
import subprocess
from custom_exit import exit
from exit_codes import *
import tempfile
from checker_manager import CheckerManager

def print_help():
    with tempfile.TemporaryFile("w") as f:
        if subprocess.call(["man", "BANANA-tree"], stderr=f):
            return (EXIT_MAN_PAGE_NOT_FOUND, )
    return (EXIT_OK, )

def main(argv):
    if ("-h" in argv) or ("--help" in argv):
        return print_help()
    if "--update" in argv or "-u" in argv:
        subprocess.Popen([os.path.dirname(os.readlink(__file__)) + "/../update.sh"])
        return (EXIT_OK,)
    manager = CheckerManager(argv)
    if manager.check():
        return (EXIT_INVALID_PATH, manager.path)
    return (EXIT_OK,)

if __name__ == '__main__':
    exit(*main(sys.argv))