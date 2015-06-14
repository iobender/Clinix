# ls.py
# emulates the ls program

import clinix
import os

class LsOutput(clinix.ClinixOutput):
    """
    class LsOutput(ClinixOutput)

    represents output from ls
    """

    def __init__(self, output):
        self.output = output

    def __str__(self):
        def singlestr(arg):
            if arg[0] == 'file':
                return arg[1]
            elif arg[0] == 'directory':
                return arg[1] + ':\n\t' + '\n\t'.join(arg[2])
        return '\n'.join(singlestr(arg) for arg in self.output)

def ls(*args, **options):
    """
    ls(*args, **options)

    lists directory contents

    args should be a list of files/directories to process
    if args is empty, a sole argument '.' is assumed

    A list is returned, with elements as follows:
        if an arg was a file, just the filename 
        if an arg is a directory, a tuple of filename and list
        of files/directories in that directory 

    options is a dict of options to ls
    Valid options (with defaults):
        
    """

    # if no arguments given to ls, assume only 
    # argument is current directory (like $ls)
    if not args:
        args = ['.']

    result = [_ls_arg(arg, **options) for arg in args]
    return LsOutput(result)

def _ls_arg(arg, **options):
    if os.path.isfile(arg):
        return ('file', arg)
    elif os.path.isdir:
        return ('directory', arg, os.listdir(arg))
    else:
        raise Exception(arg + ': no such file or directory')
