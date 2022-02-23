import os
import unittest
from utils.file import is_file_hidden, goto_first_occurence_of_str, goto_line
from utils.file import goto_end_of_section

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

class TestUtilsFile_goto_line(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        self.cur_dir = os.environ.get('BANANATREE')
        if not self.cur_dir:
            raise Exception("env variable 'BANANATREE' isn't set")
        self.test_dir = self.cur_dir + "/BANANA_tree/tests/"
        self.test_files = self.test_dir + "/test_files/"

    def test_invalid_arg_n_not_int(self):
        with open("/dev/null", "r") as f:
            self.assertRaises(TypeError, goto_line, "42", f)

    def test_invalid_arg_start_not_int(self):
        with open("/dev/null", "r") as f:
            self.assertRaises(TypeError, goto_line, 42, f, "42")

    def test_invalid_arg_f_not_textiowrapper(self):
        self.assertRaises(TypeError, goto_line, 42, 42)

    def test_return_value(self):
        with open(self.test_files + "/numbered_line_15") as f:
            return_value = goto_line(14, f)
            self.assertEqual(return_value, "14\n")

    def test_next_readline_value(self):
        with open(self.test_files + "/numbered_line_15") as f:
            goto_line(10, f)
            self.assertEqual(f.readline(), "11\n")

    def test_start_ne_1_return_value(self):
        with open(self.test_files + "/numbered_line_15") as f:
            while not f.readline() == "8\n":
                pass
            return_value = goto_line(14, f, 9)
            self.assertEqual(return_value, "14\n")

    def test_start_ne_1_next_readline_value(self):
        with open(self.test_files + "/numbered_line_15") as f:
            while not f.readline() == "8\n":
                pass
            goto_line(10, f, 9)
            self.assertEqual(f.readline(), "11\n")

class TestUtilsFile_goto_end_of_section(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        self.cur_dir = os.environ.get('BANANATREE')
        if not self.cur_dir:
            raise Exception("env variable 'BANANATREE' isn't set")
        self.test_dir = self.cur_dir + "/BANANA_tree/tests/"
        self.test_files = self.test_dir + "test_files/goto_end_of_section/"

    def test_invalid_arg_file_not_textiowrapper(self):
        self.assertRaises(TypeError, goto_end_of_section, 42, "a", "b")

    def test_invalid_arg_section_delimiter_not_str(self):
        with open("/dev/null") as f:
            self.assertRaises(TypeError, goto_end_of_section, f, 42, "b")
            self.assertRaises(TypeError, goto_end_of_section, f, "a", 42)

    def test_invalid_arg_first_line_not_str(self):
        with open("/dev/null") as f:
            self.assertRaises(TypeError, goto_end_of_section, f, "a", "b", 42)

    def test_invalid_arg_starting_section_level_not_int(self):
        with open("/dev/null") as f:
            self.assertRaises(TypeError, goto_end_of_section, f, "a", "b", "", "")

    def test_simple_section(self):
        with open(self.test_files + "simple_section") as f:
            f.readline()
            self.assertEqual(goto_end_of_section(f, "a", "b"), 4)
            self.assertEqual(f.readline(), "END")

    def test_simple_section_one_line(self):
        with open(self.test_files + "simple_section_one_line") as f:
            first_line = f.readline()
            self.assertEqual(goto_end_of_section(f, "a", "b", first_line, starting_section_level=0), 0)
            self.assertEqual(f.readline(), "END")

    def test_section_dont_end(self):
        with open(self.test_files + "section_not_closed") as f:
            self.assertRaises(EOFError, goto_end_of_section, f, "a", "b")

    def test_section_start_gt_1(self):
        with open(self.test_files + "section_start_lvl_3") as f:
            self.assertEqual(
                goto_end_of_section(f, "a", "b",starting_section_level=3),
                4
            )