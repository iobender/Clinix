# ls.py
# emulates the ls program

import clinix
import os

class LsCommand(clinix.ClinixCommand):
    """
    class LsCommand(clinix.ClinixCommand)

    Class to represent an ls command
    """

    def __init__(self, args, options):
        """
        __init__(self, args, options)

        args is a list of files and directories to process
        if files are given, use . (the current directory) as the only arg
        options is a dict of options to ls
        """

        super().__init__(options)

        if not args:
            args = ['.']
        self.filenames = args

    def _parse_options(self, options):
        """
        _parse_options(self, options)

        parses the options given to ls
        """

        pass

    def _ls_one(self, arg):
        """
        _ls_one(self, arg)

        Processes a single argument to ls
        arg can be either a file or directory
        if it is a file, just list the file
        if it is a dir, list all the files and directories in it
        """

        # TODO: use namedtuples
        if os.path.isfile(arg):
            return ('file', arg)
        elif os.path.isdir:
            return ('directory', arg, os.listdir(arg))
        else:
            raise Exception(arg + ': no such file or directory')

    def __str__(self):
        """
        __str__(self)

        Returns the output from this ls command
        files are printed by their names
        diretcories are printed by their name and then
        everything within them 
        """

        def singlestr(arg):
            if arg[0] == 'file':
                return arg[1]
            elif arg[0] == 'directory':
                return arg[1] + ':\n\t' + '\n\t'.join(arg[2])

        result = [self._ls_one(arg) for arg in self.filenames]
        return '\n'.join(singlestr(arg) for arg in result)

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

    return LsCommand(args, options)

