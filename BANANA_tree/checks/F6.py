from checks.check_report import CheckReport
from .checker import Checker
from globals import *
from utils.function import Function
import re

SIMPLE_COMMENT_PATTERN = re.compile(
    r"//",
    re.MULTILINE
)
MULTILINE_COMMENT_START_PATTERN = re.compile(
    r"\/\*",
    re.MULTILINE
)

class F6Checker(Checker):
    def __init__(self):
        super().__init__("F6", severity=MINOR)
        self.description = "Comments inside a function"

    def check(self, filename:str, functions:list[Function], **kwargs) -> list[CheckReport]:
        if not functions:
            return []
        errors = []
        for function in functions:
            body = function.string.find('{')
            simple_comments = SIMPLE_COMMENT_PATTERN.finditer(function.string)
            multiline_comments = MULTILINE_COMMENT_START_PATTERN.finditer(function.string)
            if not simple_comments:
                continue
            for comment in simple_comments:
                starty = function.string.count('\n', 0, comment.start()) + function.start
                errors.append(CheckReport(filename, [starty, 0], range(0, 1),
                self.error_type, self.severity, self.description))
            for comment in multiline_comments:
                start_line = comment.string.count('\n', 0, comment.start())
                stop_line_idx = comment.string.find("*/", 0, -1)
                stop_line = comment.string.count('\n', comment.start(), stop_line_idx) + start_line
                for line in range(stop_line - start_line + 1):
                    starty = start_line + line + function.start
                    errors.append(CheckReport(filename, [starty, 0], range(0, 1),
                    self.error_type, self.severity, self.description))
        return errors
