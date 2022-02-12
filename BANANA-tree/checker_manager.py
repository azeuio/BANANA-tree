from math import ceil
import checks
import os
from globals import MAJOR, MINOR, INFO
from utils.path import is_file_hidden

class CheckerManager:
    CHECKERS:tuple[checks.Checker] = (
        checks.F3Checker(),
    )

    def __init__(self):
        pass

    def check_file(self, filename):
        if not (os.path.exists(filename) and os.path.isfile(filename)):
            return []
        error_reports:list[checks.CheckReport] = []
        for checker in CheckerManager.CHECKERS:
            report = checker.check(filename)
            if report:
                error_reports.append(report)
        if len(error_reports):
            error_reports.sort(key=lambda x: x[0].error_type)
        return error_reports

    def _get_severity_str(self, report:checks.CheckReport):
        severity = "\33[47;30mUNKNOWN\33[m"
        if report.severity == MAJOR:
            severity = "\33[41m MAJOR \33[m"
        if report.severity == MINOR:
            severity = "\33[43;30m MINOR \33[m"
        if report.severity == INFO:
            severity = "\33[46;30m INFO \33[m"
        return severity


    def _print_reports_list(self, file_reports:list[list[list[checks.CheckReport]]]):
        if len(file_reports) == 0 or sum(len(e) for e in file_reports) == 0:
            print("Nothing to report! 🥳🎉")
            return
        longuest_filename = "."
        for reports in file_reports:
            if len(reports):
                if len(reports[0][0].filename) > len(longuest_filename):
                    print(reports[0][0].filename)
                    longuest_filename = reports[0][0].filename
        width_column_filename = len(longuest_filename)
        for file_report in file_reports:
            if file_report and file_report[0]:
                print(f"\n===== {file_report[0][0].filename} =====")
            for reports in file_report:
                for i, line in enumerate(reports):
                    position = f"{line.error_pos[0]}:{line.error_pos[1]}"
                    name_and_pos = f"{reports[0].filename}:{position}"
                    print(name_and_pos, end="")
                    for _ in range(max(0, 1 + round((width_column_filename - len(name_and_pos)) / 8))):
                        print("\t", end="")
                    print(f"\t\t{reports[0].error_type}", end="")
                    print(f"\t{self._get_severity_str(line)}")

    def _print_reports(self, path:str, file_reports:list[list[list[checks.CheckReport]]]):
        self._print_reports_list(file_reports)

    def _get_reports(self, path:str):
        if (is_file_hidden(path) == 1):
            return []
        file_reports:list[list[list[checks.CheckReport]]] = []
        if os.path.isfile(path):
            file_reports = [self.check_file(path)]
        elif os.path.isdir(path):
            for file in os.listdir(path):
                file = str(path.removesuffix("/") + "/" + file)
                if (os.path.isdir(file)):
                    file_reports.extend(self._get_reports(file))
                else:
                    file_reports.append(self.check_file(file))
        return file_reports

    def check(self, path):
        if not os.path.exists(path):
            return False
        file_reports = self._get_reports(path)
        self._print_reports(path, file_reports)
