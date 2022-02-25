from checks.check_report import CheckReport
from .checker import Checker
from globals import *
from utils.function import Function
import re

SNAKE_CASE_PATTERN:re.Pattern = re.compile(
    r"[a-z\_]+"
)

class F2Checker(Checker):
    def __init__(self):
        super().__init__("F2", severity=MAJOR)
        self.description = "Naming functions"

    def check(self, filename:str, functions:list[Function], **kwargs) -> list[CheckReport]:
        if not functions:
            return []
        errors = []
        for function in functions:
            first_line = function.string.splitlines()[0]
            name = first_line.split('(')[0].split(' ')[-1].removesuffix('\\')
            if not SNAKE_CASE_PATTERN.fullmatch(name):
                errors.append(CheckReport(filename,
                [function.start, first_line.find(name) + 1],
                range(function.body_start, function.stop), self.error_type,
                self.severity, self.description))
        return errors
