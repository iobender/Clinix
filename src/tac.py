# tac.py
# emulates the tac tool

import clinix
from collections import namedtuple

TacSuccess = namedtuple('TacSuccess', 'file contents')
TacError = namedtuple('TacError', 'file reason')

class TacCommand(clinix.ClinixCommand):
    """
    Class to represent a tac command
    """

    def __init__(self, args, options):
        """
        args is a list of files to output 
        options is a dict of options to tac
        """

        super().__init__(options)
        self.filenames = args

    def parse_options(self, options):
        """
        parses the options given to tac
        """

        pass

    def tac_one(self, filename):
        """
        tac's a single file

        returns either TacSuccess or TacError
        """

        try:
            with open(filename) as f:
                lines = f.read().splitlines()
                lines = self.tac_lines(lines)
                return TacSuccess(filename, '\n'.join(lines))
        except IOError as e:
            return TacError(filename, e.strerror)

    def tac_lines(self, lines):
        """
        tac's the given lines

        takes a list and returns a list
        """

        return reversed(lines)

    def tac_stdin(self):
        """
        tac's stdin

        Currently always returns TacSuccess
        """

        return TacSuccess('-', '\n'.join(self.tac_lines(self.read_stdin().splitlines())))

    def eval(self):
        """
        returns a Python representation of the result of this command

        for tac, return the output of the given files, with the order of lines reversed
        """

        filenames = clinix.expand_files(self.filenames)
        if filenames:
            return [self.tac_one(f) for f in filenames]
        else:
            return [self.tac_stdin()]

    def __str__(self):
        """
        Outputs the given files with their line orders reversed
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
    outputs the contents of the passed files, with line order reversed

    options is a dict of options to tac
    Valid options (with defaults):

    """

    return TacCommand(args, options)
