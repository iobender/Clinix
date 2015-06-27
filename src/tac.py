# echo.py
# emulates the echo tool

import clinix
from collections import namedtuple

TacSuccess = namedtuple('TacSuccess', 'file contents')
TacError = namedtuple('TacError', 'file reason')

class TacCommand(clinix.ClinixCommand):
    """
    class TacCommand(clinix.ClinixCommand)

    Class to represent a tac command
    """

    def __init__(self, args, options):
        """
        __init__(self, args, options)

        args is a list of files to output 
        options is a dict of options to tac
        """

        super().__init__(options)
        self.filenames = args

    def parse_options(self, options):
        """
        _parse_options(self, options)

        parses the options given to echo
        """

        pass

    def tac_one(self, filename):
        """
        tac_one(self, filename)

        tac's a single file
        returns either TacSuccess or TacError
        """

        try:
            with open(filename) as f:
                lines = reversed(f.read().splitlines())
                return TacSuccess(filename, '\n'.join(lines))
        except IOError as e:
            return TacError(filename, e.strerror)


    def eval(self):
        """
        eval(self)

        returns a Python representation of the result of this command
        for echo, just return's its arguments
        """

        return [self.tac_one(f) for f in self.filenames]

    def __str__(self):
        """
        __str__(self)

        Outputs each of the args given to echo, one per line,
        although each object may take up more than one line
        """
        
        def singlestr(arg):
            if isinstance(arg, TacSuccess):
                return arg.contents
            elif isinstance(arg, TacError):
                return arg.file + ': ' + arg.reason
            else:
                raise Exception("Don't know how to handle tac result " + arg.__class__.__name__)

        return '\n'.join(singlestr(arg) for arg in self.eval())

def tac(*args, **options):
    """
    tac(*args, **options)

    outputs the contents of the passed files

    options is a dict of options to echo
    Valid options (with defaults):

    """

    return TacCommand(args, options)
