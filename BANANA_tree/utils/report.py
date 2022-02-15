import checks

def file_has_error(filename, file_reports:list[list[list[checks.CheckReport]]]):
    """
    Returns `True` if `file_report` contains a report about `filename`
    """
    for file_report in file_reports:
        for reports in file_report:
            if reports and reports[0]:
                if reports[0].filename == filename:
                    return True
    return False