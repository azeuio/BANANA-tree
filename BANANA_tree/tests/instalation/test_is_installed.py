#!/usr/bin/env python3
import unittest
import os

class TestIsInstalled(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_is_link_in_bin_directory(self):
        path = os.environ["HOME"] + "/bin/BANANA-tree"
        self.assertTrue(os.path.exists(path))

    def test_is_man_page_installed(self):
        path = "/usr/local/man/man1/BANANA-tree.1.gz"
        self.assertTrue(os.path.exists(path))
