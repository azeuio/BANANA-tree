import os.path

class CheckReport:
    def __init__(self, filename, error_pos, precision_range=range(0, 1),
    error_type=None, severity=0):
        self.filename = filename
        self.error_pos:list = error_pos
        self.error_pos[0] = max(1, error_pos[0])
        while (len(self.error_pos) < 3):
            self.error_pos.append(1)
        self.precision_range = precision_range
        self.precision_range = range(
            precision_range.start,
            precision_range.stop,
            precision_range.step
        )
        self.error_type = error_type
        self.severity = severity

    def add_error_str(self, string, prefix=""):
        """"""
        string += prefix + " " * (self.error_pos[1] - (len(prefix) - 2))
        string += "\33[1;31m"
        string += '^' * (self.error_pos[2] + 1)
        string += "\33[m\n"
        return string

    def to_str(self) -> str:
        """Return string representation of where the error occurred in the file"""
        result = ""
        if not os.path.exists(self.filename):
            return result
        with open(self.filename) as f:
            f_content = f.readlines()
            try:
                start = max(0, self.error_pos[0] + self.precision_range.start)
                stop = self.error_pos[0] + self.precision_range.stop
                start = max(start, 0)
                stop = min(stop, len(f_content) - 1)
                line = start
                for line in range(start, self.error_pos[0] + 1):
                    result += f"{line} {f_content[max(0, line - 1)]}"
                result = result.removesuffix("\n") + "\n"
                result = self.add_error_str(result, f"{line} ")
                for line in range(self.error_pos[0] + 1, stop):
                    result += f"{line} {f_content[line - 1]}"
            except IndexError:
                result = ""
        return result.removesuffix("\n")

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return repr(self)
