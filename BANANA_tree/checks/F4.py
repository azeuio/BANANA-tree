from checks.check_report import CheckReport
from .checker import Checker
from globals import *
from utils.function import Function

class F4Checker(Checker):
    def __init__(self):
        super().__init__("F4", severity=MAJOR)
        self.description = "Number of lines"

    def check(self, filename:str, functions:list[Function], **kwargs) -> list[CheckReport]:
        if not functions:
            return []
        errors = []
        for function in functions:
            if function.size > 20:
                errors.append(CheckReport(
                    filename, [function.start, function.stop],
                    range(function.start, function.stop),
                    self.error_type, self.severity, self.description)
                )
        return errors
