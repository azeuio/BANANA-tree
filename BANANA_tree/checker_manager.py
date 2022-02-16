from custom_exit import exit
from exit_codes import EXIT_INVALID_PARAMETER
import checks
import os
from globals import MAJOR, MINOR, INFO
from utils.path import is_file_hidden
from utils.report import file_has_error

TYPE_COL_W = 4
SEVERITY_COL_W = 15
DESC_COL_W = 40

class CheckerManager:
    CHECKERS:tuple[checks.Checker] = (
        checks.F3Checker(),
    )

    def __init__(self, argv:list[str]):
        options_list = [arg for arg in argv if arg.startswith('-')]
        options_list = self.__parse_options(options_list)
        options_dict = self.__create_options_dict(options_list)
        self.__set_options(options_dict)
        self.__check_options_validity(argv)
        self.__set_default_searching_directory(tuple(arg for arg in argv if not arg.startswith("-")))
        self.filename_col_w = 0

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
            if option == "-r":
                options[i] = "--recursive"
        return options

    def __set_options(self, options_dict:dict):
        self.view = options_dict.get("--view") or "list"
        self.recursive = options_dict.get("--recursive", None) is not None

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
        len_list = len(options_list) - 1
        for i, opt in enumerate(options_list):
            if not opt.startswith("-"):
                continue
            if i < len_list and not options_list[i + 1].startswith("-"):
                options_dict[opt] = options_list[i + 1]
            else:
                options_dict[opt] = ""
        return options_dict

    def check_file(self, filename):
        if not (os.path.exists(filename) and os.path.isfile(filename)):
            return []
        error_reports:list[checks.CheckReport] = []
        for checker in CheckerManager.CHECKERS:
            report = checker.check(filename)
            if report:
                error_reports.append(report)
        if len(error_reports):
            error_reports.sort(key=lambda x: x[0].error_type.error_type)
        return error_reports

    def __get_severity_str(self, report:checks.CheckReport):
        severity = "UNKNOWN"
        if report.error_type.severity == MAJOR:
            severity = " MAJOR "
        if report.error_type.severity == MINOR:
            severity = " MINOR "
        if report.error_type.severity == INFO:
            severity = " INFO "
        return severity

    def __get_severity_color(self, severity:str) -> str:
        if " MAJOR " in severity:
            return "\33[41m"
        if " MINOR " in severity:
            return "\33[43;30m"
        if " INFO " in severity:
            return "\33[46;30m"
        return "\33[47;30m"

    def _get_severity(self, report:checks.CheckReport) -> str:
        severity = self.__get_severity_str(report)
        severity_colored = self.__get_severity_color(severity) + severity + "\33[m"
        severity = severity.center(SEVERITY_COL_W).replace(severity, severity_colored)
        return severity

    def _get_type(self, report:checks.CheckReport) -> str:
        return report.error_type.error_type

    def _get_name_and_pos(self, report:checks.CheckReport) -> str:
        position = f"{report.error_pos[0]}:{report.error_pos[1]}"
        name_and_pos = f"{report.filename}:{position}"
        return name_and_pos

    def __print_list_view_header(self):
        print(f"\33[40m{'NAME AND POSITION'.center(self.filename_col_w)}", end="")
        print(f"{'TYPE'.center(TYPE_COL_W)}", end="")
        print(f"{'SEVERITY'.center(SEVERITY_COL_W)}", end="")
        print(f"{'DESCRIPTION'.center(DESC_COL_W)}", end="")
        print("\33[m")

    def _print_list_view_line(self, filename:str, type:str, severity:str, description:str):
        print(filename.ljust(self.filename_col_w), end="")
        print(type.center(TYPE_COL_W), end="")
        print(severity.center(SEVERITY_COL_W), end="")
        print(description.center(DESC_COL_W))

    def print_reports_list(self, file_reports:list[list[list[checks.CheckReport]]]):
        if len(file_reports) == 0 or sum(len(e) for e in file_reports) == 0:
            print("Nothing to report! 🥳🎉")
            return
        longuest_filename = "."
        for reports in file_reports:
            if len(reports):
                if len(reports[0][0].filename) > len(longuest_filename):
                    longuest_filename = reports[0][0].filename
        self.filename_col_w = len(longuest_filename) + 16
        self.__print_list_view_header()
        for file_report in file_reports:
            if file_report and file_report[0]:
                print()
                print(end="\33[1m")
                filename = f"─── {file_report[0][0].filename} ───".center(self.filename_col_w)
                self._print_list_view_line(
                    filename +
                    "" * (self.filename_col_w - len(filename)),
                    "" * TYPE_COL_W, "" * SEVERITY_COL_W, "" * DESC_COL_W)
                print(end="\33[m")
            for reports in file_report:
                for report in reports:
                    self._print_list_view_line(
                        self._get_name_and_pos(report),
                        self._get_type(report),
                        self._get_severity(report),
                        report.error_type.description
                    )

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
            if (os.path.isdir(file)) and self.recursive:
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
            self.print_reports_list(file_reports)
        elif self.view == "tree":
            self.print_reports_tree_view(path, file_reports)

    def get_reports(self, path:str):
        if (is_file_hidden(path) == 1):
            return []
        file_reports:list[list[list[checks.CheckReport]]] = []
        if os.path.isfile(path):
            file_reports = [self.check_file(path)]
        elif os.path.isdir(path) and (self.recursive or path == self.path):
            for file in os.listdir(path):
                file = str(path.removesuffix("/") + "/" + file)
                if (os.path.isdir(file)):
                    file_reports.extend(self.get_reports(file))
                else:
                    file_reports.append(self.check_file(file))
        return file_reports

    def check(self):
        if not os.path.exists(self.path):
            return 1
        if os.path.isdir(self.path):
            self.path = self.path.removesuffix("/") + "/"
        self.path = self.path
        file_reports = self.get_reports(self.path)
        self.print_reports(self.path, file_reports)
        return 0
