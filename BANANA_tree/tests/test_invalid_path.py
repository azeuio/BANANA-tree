#!/usr/bin/env python3
import subprocess
import sys
import unittest
from main import main
from exit_codes import *
from utils.redirect import captured_output

class TestInvalidPath(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_return_value(self):
        with captured_output() as _:
            exit_status = main(["BANANA-tree", "file/that/does/not/exist"])
            self.assertEqual(exit_status, (EXIT_INVALID_PATH, "file/that/does/not/exist"))

    def test_exit_message(self):
        process = subprocess.Popen(["BANANA-tree", "do/not/exist"], stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        stderr = stderr.decode(sys.stdin.encoding)
        self.assertEqual(stderr, "'do/not/exist' is not a valid path\n")

    def test_exit_status(self):
        process = subprocess.Popen(["BANANA-tree", "do/not/exist"], stderr=subprocess.PIPE)
        _, _ = process.communicate()
        process.wait(5)
        self.assertEqual(process.returncode, 1)

    def test_no_parameter_return_value(self):
        with captured_output() as _:
            exit_status = main(["BANANA-tree"])
            self.assertEqual(exit_status, (EXIT_OK, ))

    def test_no_parameter_exit_message(self):
        process = subprocess.Popen(["BANANA-tree"], stdout=subprocess.PIPE)
        _, stderr = process.communicate()
        self.assertEqual(stderr, None)

    def test_no_parameter_exit_status(self):
        process = subprocess.Popen(["BANANA-tree"], stdout=subprocess.PIPE)
        _, _ = process.communicate()
        process.wait(5)
        self.assertEqual(process.returncode, 0)
