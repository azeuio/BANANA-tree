from dataclasses import dataclass
from functools import cache, cached_property
from checks.check_report import CheckReport


@dataclass(init=False)
class FileReport:
    """
    A list of `CheckReport` with added functions.

    ### Warning
        Only interact with this class once you set all reports in its `reports`
        attribute.

        Since most of this class functions/attributes are computationally
        expensive they are only computed once before being cached
    """
    reports:list[CheckReport]
    filename:str

    def __init__(self, filename:str):
        self.reports = []
        self.filename = filename

    def __iter__(self):
        return iter(self.reports)

    def __len__(self):
        return len(self.reports)

    @cache
    def sorted(self, key=None, reverse:bool=False):
        return sorted(self.reports, key=key, reverse=reverse)

    @cache
    def sorted_in_list(self, key=None, reverse:bool=False) -> list[list[CheckReport]]:
        sorted_ = self.sorted(key=key, reverse=reverse)
        result = [[]]
        prev_key_result = key(sorted_[0])
        for elem in sorted_:
            if key(elem) == prev_key_result:
                result[-1].append(elem)
                continue
            prev_key_result = key(elem)
            result.append([key(elem)])
        return result
