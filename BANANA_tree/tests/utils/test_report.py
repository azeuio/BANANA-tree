import unittest
from random import randint, choice, randrange
from checks.file_report import FileReport
from checks.check_report import CheckReport
from utils.report import file_has_error

class TestUtilsReport_file_has_error(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def __create_file_report(filename:str, n_type:int, n_report_per_type:range):
        result = FileReport(filename)
        letters = tuple(chr(letter + ord('A')) for letter in range(n_type))
        numbers = tuple(chr(randint(0, 9) + ord('0')) for _ in range(n_type))
        types = list(zip(letters, numbers))
        for _ in range(n_type):
            result.reports.append([])
            type_ = choice(types)
            types.remove(type_)
            for _ in range(randrange(n_report_per_type.start, n_report_per_type.stop) + 1):
                result.reports[-1].append(CheckReport(filename, [randint(0, 80),randint(0, 80)]))
        return result

    def test_no_report(self):
        self.assertFalse(file_has_error("filename", []))

    def test_no_report_about_file(self):
        file_reports = [self.__create_file_report("other_file", 1, range(1, 2))]
        self.assertFalse(file_has_error("filename", file_reports))

    def test_one_report_about_file(self):
        file_reports = [self.__create_file_report("filename", 1, range(1, 2))]
        self.assertTrue(file_has_error("filename", file_reports))

    def test_multiple_report_about_file(self):
        file_reports = [
            self.__create_file_report("filename", 1, range(5)),
            self.__create_file_report("filename", 1, range(5)),
            ]
        self.assertTrue(file_has_error("filename", file_reports))

    def test_one_report_about_file_among_multiple(self):
        file_reports = [
            self.__create_file_report("filename", 1, range(1, 2)),
            self.__create_file_report("other_file", 1, range(1, 2)),
            self.__create_file_report("another_one", 1, range(1, 2)),
            ]
        self.assertTrue(file_has_error("filename", file_reports))

    def test_filename_not_string(self):
        self.assertRaises(TypeError, file_has_error(3, []))

    def test_file_reports_contains_non_valid_element(self):
        file_reports = file_has_error("filename",
        [
            self.__create_file_report("filename", 1, range(1)),
            "not a FileReport",
            self.__create_file_report("other_file", 1, range(1)),
        ])
        self.assertRaises(TypeError, file_has_error("filename", file_reports))

    def test_file_reports_is_not_an_iterable(self):
        self.assertRaises(TypeError, file_has_error("filename", 42))