import unittest
from utils.file import is_file_hidden

class TestUtilsFile_is_file_hidden(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_non_hidden_file(self):
        return_value = is_file_hidden("tests/test_files/not_hidden_file")
        self.assertEqual(return_value, False)

    def test_hidden_file(self):
        return_value = is_file_hidden("tests/test_files/.hidden_file")
        self.assertEqual(return_value, True)

    def test_non_hidden_folder(self):
        return_value = is_file_hidden("tests/test_files/not_hidden_folder")
        self.assertEqual(return_value, False)

    def test_hidden_folder(self):
        return_value = is_file_hidden("tests/test_files/.hidden_folder")
        self.assertEqual(return_value, True)