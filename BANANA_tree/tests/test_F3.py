#!/usr/bin/env python3
import unittest
from checks.check_report import CheckReport
from checks.F3 import F3Checker

class TestF3(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        self.f3 = F3Checker()

    def test_valid_simple(self):
        cur_dir = __file__.removesuffix(__file__.split('/')[-1])
        path = f"{cur_dir}test_files/F3/valid_simple"
        return_value = self.f3.check(path)
        self.assertEqual(return_value, [])

    def test_invalid_simple(self):
        cur_dir = __file__.removesuffix(__file__.split('/')[-1])
        path = f"{cur_dir}test_files/F3/invalid_simple"
        return_value = self.f3.check(path)
        self.assertIsInstance(return_value, list)
        self.assertIsInstance(return_value[0], CheckReport)

    def test_valid_complex_tab(self):
        cur_dir = __file__.removesuffix(__file__.split('/')[-1])
        path = f"{cur_dir}test_files/F3/valid_complex_tab"
        return_value = self.f3.check(path)
        self.assertEqual(return_value, [])

    def test_invalid_complex_tab(self):
        cur_dir = __file__.removesuffix(__file__.split('/')[-1])
        path = f"{cur_dir}test_files/F3/invalid_complex_tab"
        return_value = self.f3.check(path)
        self.assertIsInstance(return_value, list)
        self.assertIsInstance(return_value[0], CheckReport)

    def test_valid_empty(self):
        cur_dir = __file__.removesuffix(__file__.split('/')[-1])
        path = f"{cur_dir}test_files/empty_file"
        return_value = self.f3.check(path)
        self.assertEqual(return_value, [])