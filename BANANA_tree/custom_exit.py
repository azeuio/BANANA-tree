from asyncore import write
import sys
from exit_codes import *

EXIT_MESSAGES:dict[int,str] = {
    EXIT_OK:"",
    EXIT_COMMON_ERROR:"An error occured",
    EXIT_MAN_PAGE_NOT_FOUND:"Man page was not found",
    EXIT_INVALID_PATH:"'{0}' is not a valid path",
    EXIT_INVALID_PARAMETER:"Parameter '{0}' received an invalid value ({1})"
}

def exit(exit_code=0, *format):
    """
    Exit program using `exit code`

    * If exit_code is a key of `EXIT_CODES`, its corresponding message will be printed.
    * Any value needed by the message to format it is to be passed as additional arguments.
    """
    if not isinstance(exit_code, int):
        sys.stderr.write("Wrong exit code\n")
        exit(1)
    if EXIT_MESSAGES.get(exit_code, -1) != -1:
        if EXIT_MESSAGES[exit_code]:
            sys.stderr.write(EXIT_MESSAGES[exit_code].format(*format) + "\n")
    else:
        sys.stderr.write(EXIT_MESSAGES[EXIT_COMMON_ERROR] + "\n")
    sys.exit(exit_code != EXIT_OK)