from io import TextIOWrapper


def is_file_hidden(filepath:str) -> bool:
    """
    Returns whether or not a file is hidden.
    ### Return Values:
    * `1` if the file is hidden.
    * `0` otherwise.

    #### special case
    * Returns `2` if the hidden file is `./` or `../`,
    """
    filepath = filepath.removesuffix("/")
    if filepath in (".", ".."):
        return 2
    return filepath.split("/")[-1].startswith(".")

def goto_first_occurence_of_str(str_:str, file:TextIOWrapper) -> int:
        """
        Execute `file.readline()` until `str_` is found.
        ### Return:
        Returns the number of line read
        """
        if not isinstance(str_, str) or not isinstance(file, TextIOWrapper):
            raise TypeError
        line_read = 1
        line = file.readline()
        while not str_ in line:
            line = file.readline()
            if not line:
                break
            line_read += 1
        return line_read

def goto_line(n:int, file:TextIOWrapper, start:int=1) -> str:
        """
        After call, `file.readline()` will return the (n+1)th line of `file`
        This function assumes that next call of `file.readline()` will return
        the content of the `start`th line
        ### Return:
        Returns the nth line of file
        """
        if (not (isinstance(file,TextIOWrapper) and isinstance(n,int) and
        isinstance(start,int))):
            raise TypeError

        for _ in range(start - 1, n):
            line = file.readline()
        return line

def goto_end_of_section(file:TextIOWrapper, section_start:str,
section_end:str, starting_line:str="", starting_section_level:int=1) -> int:
    """
    After call, `file.readline()` will return the first line after the section
    that starts with `section_start` and ends with `section_end`.

    Sub-sections can exist within the main section
    ### Return:
    Returns the length of the section, including the line contining the section
    delimiters
    """
    if (not isinstance(file, TextIOWrapper) or
    not isinstance(section_start, str) or not isinstance(section_end, str)
    or not isinstance(starting_section_level, int) or not
    isinstance(starting_line, str)):
        raise TypeError

    recursion_level = starting_section_level
    number_line_read = 0
    line = starting_line
    while recursion_level > 0:
        recursion_level -= line.count(section_end)
        recursion_level += line.count(section_start)
        if recursion_level <= 0:
            break
        line = file.readline()
        number_line_read += 1
        if not line and recursion_level > 0:
            raise EOFError(
                f"A section('{section_start}...{section_end}') "
                f"was not closed in '{file.name}'\n{recursion_level=}")
    if line == starting_line and line != "":
        return 0
    return number_line_read + 1
