from .file_report import FileReport

class Checker:
    def __init__(self, error_type=None, severity=0):
        self.error_type = error_type
        self.severity = severity
        self.description = ""

    def check(self, filename) -> FileReport:
        """
        Checks file at `filename` for any `self.error_type` error

        #### Returns:
        * `CheckReport` type object if an error found,
        * `None` otherwise
        """
        raise NotImplementedError