# ls.py
# Emulating the ls program

import os

def ls(*entries, **options):
    """
    ls(*entries, **options)

    lists directory contents

    Entries should be a list of files/directories to process
    if entries is empty, a sole argument '.' is assumed

    A list is returned, with elements as follows:
    if an entry was a file, just the filename 
    if an entry is a directory, a tuple of filename and list
    of files/directories in that directory 

    If only 1 entry is given (or none in which case the one entry),
    then a list is not returned, and instead just that one element

    options is a dict of options to ls
    Valid options (with defaults):
        
    """

    # if no arguments given to ls, assume only 
    # argument is current directory (like $ls)
    if not entries:
        entries = ['.']

    if len(entries) == 1:
        result = _ls_entry(entries[0], **options)
    else:
        result = [_ls_entry(entry, **options) for entry in entries]

    return result

def _ls_entry(entry, **options):
    if os.path.isfile(entry):
        return entry
    elif os.path.isdir:
        return (entry, os.listdir(entry))
    else:
        raise Exception(entry + ': no such file or directory')
