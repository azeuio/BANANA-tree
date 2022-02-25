import os
from .checker import Checker
from .check_report import CheckReport
from globals import *
import re


C_HEADER_PATTERN:str = re.compile(
    r"\/\*\n"
    r"\*\* EPITECH PROJECT, \d{4}\n"
    r"\*\*[ ]{0,1}.*\n"
    r"\*\* File description:\n"
    r"(\*\*.*\n)+"
    r"\*\/\n"
    )

MAKEFILE_HEADER_PATTERN:str = re.compile(
    r"\#\#\n"
    r"\#\# EPITECH PROJECT, \d{4}\n"
    r"\#\#[ ]{0,1}.*\n"
    r"\#\# File description:\n"
    r"(\#\#.*\n)+?"
    r"\#\#\n"
    )

class G1Checker(Checker):
    def __init__(self):
        super().__init__("G1", severity=MAJOR)
        self.description = "File header"

    def _is_c_file_type_header_valid(self, filename:str) -> list[CheckReport]:
        lines = []
        with open(filename, "r") as f:
            lines.append(f.readline())
            i = 0
            while lines[-1][1] == '*' and i < 20:
                lines.append(f.readline())
                if lines[-1] == "":
                    return False
                i += 1
            lines = ''.join(lines)
        c_header_pattern:re.Pattern = re.compile(C_HEADER_PATTERN)
        if not c_header_pattern.search(lines):
            return False
        return True

    def _check_c_file_type_header(self, filename:str) -> list[CheckReport]:
        if not self._is_c_file_type_header_valid(filename):
            return [CheckReport(
                filename, [0,0], error_type=self.error_type,
                severity=self.severity, description=self.description)
            ]
        return []

    def _is_makefile_type_header_valid(self, filename:str) -> list[CheckReport]:
        lines = []
        with open(filename, "r") as f:
            lines.append(f.readline())
            i = 0
            while lines[-1] != '\n' and lines[-1][1] == '#' and i < 20:
                lines.append(f.readline())
                if lines[-1] == "":
                    return False
                i += 1
            lines = ''.join(lines)
        makefile_header_pattern:re.Pattern = re.compile(MAKEFILE_HEADER_PATTERN)
        if not makefile_header_pattern.search(lines):
            return False
        return True

    def _check_makefile_type_header(self, filename:str) -> list[CheckReport]:
        if not self._is_makefile_type_header_valid(filename):
            return [CheckReport(
                filename, [0,0], error_type=self.error_type,
                severity=self.severity, description=self.description)
            ]
        return []

    def check(self, path:str, **kwargs) -> list[CheckReport]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"'{path}' is not a valid path")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"'{path}' is not a file")
        errors = []
        filename = os.path.basename(path)
        if (path.endswith('.c') or path.endswith('.h')):
            errors = self._check_c_file_type_header(path)
        elif (filename == "Makefile"):
            errors = self._check_makefile_type_header(path)
        return errors
