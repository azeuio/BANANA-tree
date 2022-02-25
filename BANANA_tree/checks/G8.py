import os
from .checker import Checker
from .check_report import CheckReport
from globals import *
import re


TRAILING_SPACE_PATTERN:re.Pattern = re.compile(
    r"^.*\s+\n",
    re.MULTILINE
)

class G8Checker(Checker):
    def __init__(self):
        super().__init__("G8", severity=MINOR)
        self.description = "Trailing spaces"

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
                line_number += 1
                line = f.readline()
                if TRAILING_SPACE_PATTERN.match(line):
                    errors.append(CheckReport(filename, [line_number, len(line)],
                    range(0,1), self.error_type, self.severity, self.description))
        return errors
