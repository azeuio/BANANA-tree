from checks.file_report import FileReport
from typing import Iterable, Any

def __file_has_error_parameters_are_valid(filename:Any, file_reports:Any):
    if not isinstance(filename, str):
        return False
    if not isinstance(file_reports, Iterable):
        return False
    if any(not isinstance(report, FileReport) for report in file_reports):
        return False
    return True

def file_has_error(filename:str, file_reports:Iterable[FileReport]):
    """
    Returns `True` if `file_report` contains a report about `filename`
    """
    if not __file_has_error_parameters_are_valid(filename, file_reports):
        return False
    for file_report in file_reports:
        if file_report.filename == filename:
            return True
    return False