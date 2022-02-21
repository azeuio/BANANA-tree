#!/usr/bin/env python3
import os
import sys
import subprocess
from utils.file_parsing.function import Function
from custom_exit import exit
from exit_codes import *
import tempfile
from checker_manager import CheckerManager
from globals import OPTIONS

def print_help():
    with tempfile.TemporaryFile("w") as f:
        if subprocess.call(["man", "BANANA-tree"], stderr=f):
            return (EXIT_MAN_PAGE_NOT_FOUND, )
    return (EXIT_OK, )

def run_test(argv:list[str]):
    banana_tree_dir = os.environ['BANANATREE']
    process = subprocess.Popen([f"{banana_tree_dir}/tests_run.sh", *argv[argv.index("--test") + 1:]])
    process.wait()
    return (EXIT_OK, )

def main(argv:list[str]):
    if ("--get-opts" in argv):
        print(' '.join(OPTIONS))
        exit(EXIT_OK)
    if ("--test" in argv):
        return run_test(argv)
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