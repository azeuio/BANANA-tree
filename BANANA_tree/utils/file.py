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
