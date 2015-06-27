# grep.py
# emulates output of the grep command

import clinix
import re
from collections import namedtuple

GrepSuccess = namedtuple('GrepSuccess', 'file line linenum')
GrepError = namedtuple('GrepError', 'file reason')

class GrepCommand(clinix.ClinixCommand):
    """
    reprsents a grep command
    """

    def __init__(self, pattern, args, options):
        """
        pattern is a regular expression to search each line for
        args is a list of files to search
        options is a dict of options to grep
        """

        super().__init__(options)
        self.compile_pattern(pattern)
        self.filenames = args

    def parse_options(self, options):
        """
        processes options to grep

        valid options are i, ignorecase, n, and linenumber
        """

        self.ignorecase = options.get('ignorecase', False) or options.get('i', False)
        self.linenumber = options.get('linenumber', False) or options.get('n', False)
        self.invertmatch = options.get('invertmatch', False) or options.get('v', False)

    def compile_pattern(self, pattern):
        """
        compiles the given regex pattern, considering the options given
        """

        flags = 0
        if self.ignorecase:
            flags |= re.IGNORECASE
        self.pattern = re.compile(pattern, flags)

    def grep_file(self, filename):
        """
        tries to open filename, and yields all matching lines

        with some info about the lines
        if the file couldn't be opened, returns an error
        """

        try:
            with open(filename) as file:
                for linenum, line in enumerate(file, 1): # count line numbers from 1
                    line = line.rstrip('\n') # remove trailing newline
                    for line in self.grep_line(line):
                        yield GrepSuccess(filename, line, linenum)
        except IOError as e:
            yield GrepError(filename, e.strerror)

    def grep_line(self, line):
        """
        returns matches found in a single line
        """

        if bool(re.search(self.pattern, line)) ^ self.invertmatch:
            yield line

    def grep_stdin(self):
        """
        reads stdin and yields matches found
        """

        for linenum, line in enumerate(self.read_stdin().splitlines()):
            for line in self.grep_line(line):
                yield GrepSuccess('<stdin>', line, linenum)

    def eval(self):
        """
        Returns a Python representation of the output of this command

        Returns a list of GrepSuccess and GrepError objects
        yields each match from each file provided, or stdin if none provided
        """

        filenames = list(clinix.expand_files(self.filenames))
        if filenames:
            for filename in filenames:
                yield from self.grep_file(filename)
        else:
            yield from self.grep_stdin()

    def __str__(self):
        """
        Returns the output of this grep command
        matches are printed on their own line, possibly with some ifo depending on the optoins given
        errors are reported with the filename and the error
        """

        def singlestr(arg):
            if isinstance(arg, GrepSuccess):
                result = ''
                if self.linenumber:
                    result += str(arg.linenum) + ':'
                result += arg.line
                return result
            elif isinstance(arg, GrepError):
                return 'grep: ' + arg.file + ': ' + arg.reason
            else:
                raise Exception("Don't know how to handle grep result " + arg.__class__.__name__)

        return '\n'.join(singlestr(arg) for arg in self.eval())

def grep(pattern, *args, **options):
    """
    searches the given files for the given pattern

    pattern is a regular expression interpretted by Python's re module

    options is a dict of options to grep
    Valid options (with defaults):
        
        i=False, ignorecase=False
            if True, does a case-insensitive search
        n=False, linenumber=False:
            if True, report the line numbers of matching lines as well
        v=False, invertmatch=False:
            if True, selects lines not matching pattern instead
    """

    return GrepCommand(pattern, args, options)
