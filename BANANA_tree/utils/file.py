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
