#!/usr/bin/env python3
import sys
import unittest
from utils.redirect import captured_output

class TestRedirect(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_output_redirected(self):
        original_output = sys.stdout
        original_error = sys.stderr
        with captured_output() as (out, err):
            self.assertNotEqual(original_output, sys.stdout)
            self.assertNotEqual(original_error, sys.stderr)

    def test_output_reset_at_exit(self):
        original_output = sys.stdout
        original_error = sys.stderr
        with captured_output() as (out, err):
            pass
        self.assertEqual(original_output, sys.stdout)
        self.assertEqual(original_error, sys.stderr)
