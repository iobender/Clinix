# ls.py
# Emulating the ls program

import os

def ls(*entries, **options):
    """
    ls(*entries, **options)

    lists directory contents

    args should be a list of files/directories to process
    if args is empty, a sole argument '.' is assumed

    kwargs is a dict of options to ls
    Valid options (with defaults):
        
    """

    # if no arguments given to ls, assume only 
    # argument is current directory (like $ls)
    if not entries:
        entries = ['.']

    result = [_ls_entry(entry, **options) for entry in entries]
    return result

def _ls_entry(entry, **options):
    if os.path.isfile(entry):
        return entry
    elif os.path.isdir:
        return (entry, os.listdir(entry))
    else:
        raise Exception(entry + ': no such file or directory')
