import os
import unittest
from utils.file import is_file_hidden, goto_first_occurence_of_str

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

class TestUtilsFile_goto_first_occurence_of_str(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        self.cur_dir = os.environ.get('BANANATREE')
        if not self.cur_dir:
            raise Exception("env variable 'BANANATREE' isn't set")
        self.test_dir = self.cur_dir + "/BANANA_tree/tests/"
        self.test_files = self.test_dir + "/test_files/"

    def test_invalid_arg_not_str(self):
        with open("/dev/null", "r") as f:
            self.assertRaises(TypeError, goto_first_occurence_of_str, 42, f)

    def test_invalid_arg_not_textiowrapper(self):
        self.assertRaises(TypeError, goto_first_occurence_of_str, "str", 42)

    def test_return_value(self):
        with open(self.test_files + "numbered_line_15") as f:
            return_value = goto_first_occurence_of_str("13", f)
            self.assertEqual(return_value, 13)

    def test_next_readline_value(self):
        with open(self.test_files + "numbered_line_15") as f:
            goto_first_occurence_of_str("13", f)
            self.assertEqual(f.readline(), "14\n")

    def test_str_not_found_return_value(self):
        with open(self.test_files + "numbered_line_15") as f:
            return_value = goto_first_occurence_of_str("not in file", f)
            self.assertEqual(return_value, 15)

    def test_str_not_found_next_readline_value(self):
        with open(self.test_files + "numbered_line_15") as f:
            goto_first_occurence_of_str("not in file", f)
            self.assertEqual(f.readline(), "")