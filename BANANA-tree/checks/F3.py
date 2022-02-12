from .checker import Checker
from .check_report import CheckReport
from globals import *

#TODO: checks tab
class F3Checker(Checker):
    def __init__(self):
        super().__init__("F3", severity=MAJOR)

    def _check_line(self, filename:str, line:str, line_number:int):
        # line = line.replace("\t", " " * TAB_LENGTH)
        while "\t" in line:
            i = line.find("\t")
            line = line[:i] + " " * (TAB_LENGTH - (i % TAB_LENGTH)) + line[i + 1:]
        errors = []
        if (len(line) >= 80):
            errors.append(CheckReport(
                filename,
                [line_number, 80, len(line) - 80],
                error_type = self.error_type,
                severity = self.severity
                ))
        return errors

    def check(self, filename):
        errors = []
        line_number = 1
        with open(filename, "r") as f:
            try:
                line = f.readline()
            except UnicodeDecodeError:
                return errors
            while line:
                line = line.removesuffix('\n')
                errors.extend(self._check_line(filename, line, line_number))
                line = f.readline()
                line_number += 1
        return errors
