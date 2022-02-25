import os
from checks.check_report import CheckReport
from .checker import Checker
from globals import *
import re

SIMPLE_COMMENT_PATTERN = re.compile(
    r"//",
    re.MULTILINE
)

class L2Checker(Checker):
    def __init__(self):
        super().__init__("L2", severity=MINOR)
        self.description = "Indentation"

    def check(self, filename:str, **kwargs) -> list[CheckReport]:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"'{filename}' is not a valid path")
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"'{filename}' is not a file")

        errors = []
        line_number = 0
        line = "START"
        with open(filename, 'r') as f:
            while line:
                line = f.readline()
                line_number += 1
                n_space = 0
                while n_space < len(line) and line[n_space] == ' ':
                    n_space += 1
                n_space = max(0, n_space)
                if n_space % TAB_LENGTH:
                    errors.append(CheckReport(filename, [line_number, 1], range(1, 0),
                    self.error_type, self.severity, self.description))
        return errors
