#!/usr/bin/env python3
import os
import unittest
from checks.check_report import CheckReport
from checks.F3 import F3Checker

class TestF3(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        self.f3 = F3Checker()
        self.cur_dir = os.environ.get('BANANATREE')
        if not self.cur_dir:
            raise Exception("env variable 'BANANATREE' isn't set")
        self.test_dir = self.cur_dir + "/BANANA_tree/tests/"

    def test_valid_simple(self):
        path = f"{self.test_dir}test_files/F3/valid_simple"
        return_value = self.f3.check(path)
        self.assertEqual(return_value, [])

    def test_invalid_simple(self):
        path = f"{self.test_dir}test_files/F3/invalid_simple"
        return_value = self.f3.check(path)
        self.assertIsInstance(return_value, list)
        self.assertIsInstance(return_value[0], CheckReport)

    def test_valid_complex_tab(self):
        path = f"{self.test_dir}test_files/F3/valid_complex_tab"
        return_value = self.f3.check(path)
        self.assertEqual(return_value, [])

    def test_invalid_complex_tab(self):
        path = f"{self.test_dir}test_files/F3/invalid_complex_tab"
        return_value = self.f3.check(path)
        self.assertIsInstance(return_value, list)
        self.assertIsInstance(return_value[0], CheckReport)

    def test_valid_empty(self):
        path = f"{self.test_dir}test_files/empty_file"
        return_value = self.f3.check(path)
        self.assertEqual(return_value, [])