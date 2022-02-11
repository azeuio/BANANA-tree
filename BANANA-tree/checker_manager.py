import checks
import os
from globals import MAJOR, MINOR, INFO

class CheckerManager:
    CHECKERS:tuple[checks.Checker] = (
    )

    def __init__(self):
        pass

    def check_file(self, filename):
        if not (os.path.exists(filename) and os.path.isfile(filename)):
            return []
        error_reports:list[checks.CheckReport] = []
        for checker in CheckerManager.CHECKERS:
            error_reports.append(checker.check(filename))
            if not error_reports[-1]:
                error_reports.pop()
        if len(error_reports):
            error_reports.sort(key=lambda x: x[0].error_type)
        return error_reports

    def _print_reports(self, file_reports:list[list[list[checks.CheckReport]]]):
        for file_report in file_reports:
            if file_report and file_report[0]:
                print(f"===== {file_report[0][0].filename} =====")
            if not file_report:
                print("Nothing to report! 🥳🎉")
            for report in file_report:
                for i, line in enumerate(report):
                    bg_color = "\33[47;30m" if i % 2 else "\33[m"
                    print(f"{file_report[0][0].filename}:", end="")
                    print(f"{line.error_pos[0]}:{line.error_pos[1]}", end="")
                    print(f"\t\t{report[0].error_type}", end="")
                    severity = "\33[47;30mUNKNOWN\33[m"
                    if report[0].severity == MAJOR:
                        severity = "\33[41m MAJOR \33[m"
                    if report[0].severity == MINOR:
                        severity = "\33[43;30m MINOR \33[m"
                    if report[0].severity == INFO:
                        severity = "\33[46;30m INFO \33[m"
                    print(f"\t\t{severity}")


    def check(self, path):
        if not os.path.exists(path):
            return False
        file_reports:list[list[list[checks.CheckReport]]] = []
        if os.path.isfile(path):
            file_reports = [self.check_file(path)]
        elif os.path.isdir(path):
            file_reports = []
            for file in os.listdir(path):
                file_reports.append(self.check_file(file))
        self._print_reports(file_reports)
