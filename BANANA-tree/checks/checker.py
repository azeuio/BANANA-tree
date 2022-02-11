from .check_report import CheckReport

class Checker:
    def __init__(self, error_type=None):
        self.error_type = error_type

    def check(self, filename):
        """
        Checks file at `filename` for any `self.error_type` error

        #### Returns:
        * `CheckReport` type object if an error found,
        * `None` otherwise
        """
        raise NotImplementedError