# cat.py
# emulates the cat tool

import clinix
from collections import namedtuple

CatSuccess = namedtuple('CatSuccess', 'file contents')
CatError = namedtuple('CatError', 'file reason')

class CatCommand(clinix.ClinixCommand):
    """
    Class to represent a cat command
    """

    def __init__(self, args, options):
        """
        args is a list of files to output 
        options is a dict of options to cat
        """

        super().__init__(options)
        self.filenames = args

    def parse_options(self, options):
        """
        parses the options given to cat
        """

        self.number = options.get('number', False) or options.get('n', False)

    def cat_one(self, filename):
        """
        cat's a single file

        returns either CatSuccess or CatError
        """

        try:
            with open(filename) as f:
                lines = f.read().splitlines()
                lines = self.cat_lines(lines)
                return CatSuccess(filename, '\n'.join(lines))
        except IOError as e:
            return CatError(filename, e.strerror)

    def cat_lines(self, lines):
        """
        returns the given lines, possibly modified based on the options to cat
        """
        if self.number:
            lines = list(enumerate(lines, 1))
            max_num_len = len(str(len(lines))) # longest length of any number (e.g. 482 -> 3)
            # 4 spaces, then line number padded with spaces on left, then 2 spaces, then actual line
            lines = [str(linenum).rjust(4 + max_num_len) + '  ' + line for linenum, line in lines]
        return lines

    def cat_stdin(self):
        """
        cat's stdin

        Currently always returns CatSucess
        """

        return CatSuccess('-', '\n'.join(self.cat_lines(self.read_stdin().splitlines())))

    def eval(self):
        """
        returns a Python representation of the result of this command
        """
    
        filenames = clinix.expand_files(self.filenames)
        if filenames:
            return [self.cat_one(f) for f in filenames]
        else:
            return [self.cat_stdin()]

    def __str__(self):
        """
        Outputs each of the files given to cat
        """
        
        def singlestr(arg):
            if isinstance(arg, CatSuccess):
                return arg.contents
            elif isinstance(arg, CatError):
                return arg.file + ': ' + arg.reason
            else:
                raise Exception("Don't know how to handle cat result " + arg.__class__.__name__)

        return '\n'.join(singlestr(arg) for arg in self.eval())

def cat(*args, **options):
    """
    outputs the contents of the passed files

    options is a dict of options to cat
    Valid options (with defaults):
        n=False, number=False:
            output line numbers as well
    """

    return CatCommand(args, options)
