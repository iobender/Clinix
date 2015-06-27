# echo.py
# emulates the echo tool

import clinix
from collections import namedtuple

RevSuccess = namedtuple('RevSuccess', 'file contents')
RevError = namedtuple('RevError', 'file reason')

class RevCommand(clinix.ClinixCommand):
    """
    class RevCommand(clinix.ClinixCommand)

    Class to represent a rev command
    """

    def __init__(self, args, options):
        """
        __init__(self, args, options)

        args is a list of files to output 
        options is a dict of options to rev
        """

        super().__init__(options)
        self.filenames = args

    def parse_options(self, options):
        """
        _parse_options(self, options)

        parses the options given to echo
        """

        pass

    def rev_one(self, filename):
        """
        rev_one(self, filename)

        rev's a single file
        returns either RevSuccess or RevError
        """

        try:
            with open(filename) as f:
                lines = self.rev_lines(f.read().splitlines())
                return RevSuccess(filename, '\n'.join(lines))
        except IOError as e:
            return RevError(filename, e.strerror)

    def rev_lines(self, lines):
        """
        rev_lines(self, lines)

        takes a list of lines and returns a list of reversed lines
        """
        lines = [''.join(reversed(line)) for line in lines]
        return lines

    def rev_stdin(self):
        """
        rev_stdin(self):

        rev's stdin
        currently always returns RevSuccess
        """
        return RevSuccess('-', '\n'.join(self.rev_lines(self.read_stdin().splitlines())))

    def eval(self):
        """
        eval(self)

        returns a Python representation of the result of this command
        for echo, just return's its arguments
        """
        if self.filenames:
            return [self.rev_one(f) for f in self.filenames]
        else:
            return [self.rev_stdin()]

    def __str__(self):
        """
        __str__(self)

        Outputs each of the args given to echo, one per line,
        although each object may take up more than one line
        """
        
        def singlestr(arg):
            if isinstance(arg, RevSuccess):
                return arg.contents
            elif isinstance(arg, RevError):
                return arg.file + ': ' + arg.reason
            else:
                raise Exception("Don't know how to handle rev result " + arg.__class__.__name__)

        return '\n'.join(singlestr(arg) for arg in self.eval())

def rev(*args, **options):
    """
    rev(*args, **options)

    outputs the contents of the passed files

    options is a dict of options to echo
    Valid options (with defaults):

    """

    return RevCommand(args, options)
