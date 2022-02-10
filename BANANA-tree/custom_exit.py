import sys
from exit_codes import *

EXIT_MESSAGES:dict[int,str] = {
    EXIT_OK:"",
    EXIT_COMMON_ERROR:"An error occured",
    EXIT_INVALID_NUMBER_OF_PARAMS:"An invalid number of parameters was passed",
    EXIT_MAN_PAGE_NOT_FOUND:"Man page was not found"
}

def exit(exit_code=0):
    """
    Exit program using `exit code`
    If exit_code is a key of `EXIT_CODES`, its corresponding message will be printed
    """
    if not isinstance(exit_code, int):
        print("Wrong exit code")
        exit(1)
    if EXIT_MESSAGES.get(exit_code, -1) != -1:
        if EXIT_MESSAGES[exit_code]:
            print(EXIT_MESSAGES[exit_code])
    else:
        print(EXIT_MESSAGES[EXIT_COMMON_ERROR])
    sys.exit(exit_code)