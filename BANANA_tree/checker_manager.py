from custom_exit import exit
from exit_codes import EXIT_INVALID_PARAMETER
import checks
import os
from globals import MAJOR, MINOR, INFO
from utils.path import is_file_hidden

class CheckerManager:
    CHECKERS:tuple[checks.Checker] = (
        checks.F3Checker(),
    )

    def __split_options_and_value(self, options:list[str]) -> list[str]:
        if not '=' in ','.join(options):
            return options
        for i, option in enumerate(options):
            if not '=' in option:
                continue
            splitting_index = option.index('=')
            split_option = option[:splitting_index], option[splitting_index+1:]
            options[i] = split_option[0]
            options.insert(i + 1, split_option[1])
        return options


    def __parse_options(self, options:list[str]):
        options = self.__split_options_and_value(options)
        for i, option in enumerate(options):
            if option == "-v":
                options[i] = "--view"
        return options

    def __set_options(self, options_dict:dict):
        self.view = options_dict.get("--view") or "list"

    def __check_options_validity(self, argv:list[str]):
        if self.view not in ("list", "tree"):
            exit(EXIT_INVALID_PARAMETER, "--view" if "--view" in argv else "-v", self.view)

    def __set_default_searching_directory(self, argv_without_options:list[str]):
        if len(argv_without_options) > 1:
            self.path = argv_without_options[1]
        else:
            self.path = "."

    def __create_options_dict(self, options_list:list[str]):
        options_dict = {}
        for i, opt in enumerate(options_list):
            if not opt.startswith("-"):
                continue
            if not options_list[i + 1].startswith("-"):
                options_dict[opt] = options_list[i + 1]
            else:
                options_dict[opt] = ""
        return options_dict

    def __init__(self, argv:list[str]):
        options_list = [arg for arg in argv if arg.startswith('-')]
        options_list = self.__parse_options(options_list)
        options_dict = self.__create_options_dict(options_list)
        self.__set_options(options_dict)
        self.__check_options_validity(argv)
        self.__set_default_searching_directory(tuple(arg for arg in argv if not arg.startswith("-")))

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

    def print_reports_tree_view(self, path:str, file_reports:list[list[list[checks.CheckReport]]]):
        if (is_file_hidden(path) == 1):
            return []
        if (path.count("/") - self.path.count("/") > 0):
            for _ in range(path.count("/") - self.path.count("/")):
                print("|  ", end="")
        if os.path.isdir(path):
            print(f"{path.removesuffix('/')}/")
        elif os.path.isfile(path):
            if file_has_error(path, file_reports):
                print(f"\33[31;1m", end="")
            print(f"{path}\33[m")
            return
        if not os.path.isdir(path):
            return
        for file in os.listdir(path):
            file = str(path.removesuffix("/") + "/" + file)
            if (os.path.isdir(file)):
                self.print_reports_tree_view(file, file_reports)
            else:
                if (file.count("/") - self.path.count("/") > 0):
                    for _ in range(file.count("/") - self.path.count("/")):
                        print("|  ", end="")
                if file_has_error(file, file_reports):
                    print(f"\33[31;1m", end="")
                print(f"{file.removesuffix('/')}\33[m")

    def print_reports(self, path:str, file_reports:list[list[list[checks.CheckReport]]]):
        if self.view == "list":
            self._print_reports_list(file_reports)
        elif self.view == "tree":
            self.print_reports_tree_view(path, file_reports)

    def get_reports(self, path:str):
        if (is_file_hidden(path) == 1):
            return []
        file_reports:list[list[list[checks.CheckReport]]] = []
        if os.path.isfile(path):
            file_reports = [self.check_file(path)]
        elif os.path.isdir(path):
            for file in os.listdir(path):
                file = str(path.removesuffix("/") + "/" + file)
                if (os.path.isdir(file)):
                    file_reports.extend(self.get_reports(file))
                else:
                    file_reports.append(self.check_file(file))
        return file_reports

    def check(self, path=""):
        if not path:
            path = self.path
        if not os.path.exists(path):
            return 1
        if os.path.isdir(path):
            path = path.removesuffix("/") + "/"
        self.path = path
        file_reports = self.get_reports(path)
        self.print_reports(path, file_reports)
        return 0
