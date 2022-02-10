from check_report import CheckReport

class Checker:
    def __init__(self):
        self.error_type = None

    def check(self, filename):
        """
        Checks file at `filename` for any `self.error_type` error

        #### Returns:
        * `CheckReport` type object if an error found,
        * `None` otherwise
        """
        raise NotImplementedError