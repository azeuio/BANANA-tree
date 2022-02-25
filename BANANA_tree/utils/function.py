from dataclasses import dataclass, field
import os
from typing import ClassVar
import utils.file as file
import re

@dataclass
class Function:
    filename:str
    start:int = 0
    type:str = None
    stop:int = field(default=-1, compare=False)
    string:str = field(default="", init=False, compare=False)
    TYPE:ClassVar[str] = 'function'
    size:int = field(default=0, init=False, compare=False)
    __TYPE_AND_NAME_PATTERN = r"^[^\n]\w+\s[\w\s]+[\\\n]*"
    __PARAM_PATTERN = r"\(" + fr"(.*(\\\n)*)*?" + r"\)[\s\n]*\{"
    FUNC_START_PATTERN:ClassVar[str] = fr"{__TYPE_AND_NAME_PATTERN}{__PARAM_PATTERN}"

    def range(self):
        return range(self.start, self.stop, self.step)

    def slice(self):
        return slice(self.start, self.stop, self.step)

    @classmethod
    def _get_function_starts_in_file(cls, filename):
        Function.function_match = re.compile(Function.FUNC_START_PATTERN, re.MULTILINE)

        result = None
        if os.stat(filename).st_size > (80 * 500):
            print(f"'{filename}' is too large. It will be ignored")
            return None
        try:
            with open(filename, 'r') as f:
                file_buffer = f.read()
                if file_buffer.count('\n') > 500:
                    print(f"'{filename}' is too large. It will be ignored")
                    return None
                match_result = cls.function_match.finditer(file_buffer)
                if match_result:
                    result = match_result
        except UnicodeDecodeError:
            return None
        return result

    @classmethod
    def create_from_line_in_file(cls, line:int, filename:str):
        new:Function = cls(filename, line, cls.type, -1)
        new.find_end()
        return new

    @classmethod
    def get_all_in_file(cls, filename):
        if (not filename.endswith(".c") or filename.endswith(".cpp")):
            return None
        functions_start = cls._get_function_starts_in_file(filename)
        if (functions_start is None):
            return None
        with open(filename, 'r') as f:
            buff = f.read()
        start_line = []
        for match_obj in functions_start:
            start_line.append(buff.count("\n", 0, match_obj.start()) + 1)
        result = [cls.create_from_line_in_file(line, filename) for line in start_line]
        return (func for func in result)

    def find_end(self):
        with open(self.filename, 'r') as f:
            file.goto_line(self.start - 1, f)
            self.body_start = self.start
            self.body_start += file.goto_first_occurence_of_str("{", f)
            self.size = file.goto_end_of_section(f, "{", "}") - 2
            self.stop = self.body_start + self.size + 1
        with open(self.filename, 'r') as f:
            file.goto_line(self.start - 1, f)
            for _ in range(self.stop - self.start):
                self.string += f.readline()
