from checks.check_report import CheckReport
from .checker import Checker
from globals import *
from utils.function import Function
import re

ALL_ARGUMENTS_PATTERN = re.compile(
    r"\b[^()]+\((.*)\)$",
    re.MULTILINE
)
ARG_PATTERN = re.compile(
    r"((?<=[\(,])[^,]+)|((?=\))[^,]+)",
    re.MULTILINE
)

class F5Checker(Checker):
    def __init__(self):
        super().__init__("F5", severity=MAJOR)
        self.description = "Arguments"

    def check(self, filename:str, functions:list[Function], **kwargs) -> list[CheckReport]:
        if not functions:
            return []
        errors = []
        for function in functions:
            arg_pattern = ALL_ARGUMENTS_PATTERN.search(function.string)
            if not arg_pattern:
                continue
            args = [''.join(e).removesuffix(')') for e in ARG_PATTERN.findall(arg_pattern.group())]
            if len(args) > 4 or (len(args) == 1 and not args[0]):
                starty = function.start
                startx = function.string.find('(') + 2
                errors.append(CheckReport(filename, [starty, startx],
                range(function.start, function.body_start), self.error_type,
                self.severity, self.description))
        return errors
