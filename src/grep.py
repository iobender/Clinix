# grep.py
# emulates output of the grep command

import clinix
import re
from collections import namedtuple

GrepSuccess = namedtuple('GrepSuccess', 'file line linenum')
GrepError = namedtuple('GrepError', 'file reason')

class GrepCommand(clinix.ClinixCommand):
    """
    class GrepCommand(ClinixCommand)

    reprsents a grep command
    """

    def __init__(self, pattern, args, options):
        """
        __init__(self, pattern, args, options)

        pattern is a regular expression to search each line for
        args is a list of files to search
        options is a dict of options to grep
        """

        super().__init__(options)
        self.compile_pattern(pattern)
        self.filenames = args

    def parse_options(self, options):
        """
        _parse_options(self, options)

        processes options to grep
        valid options are i, ignorecase, n, and linenumber
        """

        self.ignorecase = options.get('i', False) or options.get('ignorecase', False)
        self.linenumber = options.get('n', False) or options.get('linenumber', False)
        self.invertmatch = options.get('v', False) or options.get('invertmatch', False)

    def compile_pattern(self, pattern):
        """
        _compile_pattern(self, pattern)

        compiles the given regex pattern, considering the options given
        """

        flags = 0
        if self.ignorecase:
            flags |= re.IGNORECASE
        self.pattern = re.compile(pattern, flags)

    def grep_all(self):
        """
        _grep_all(self)

        yields each match from each file provided, or stdin if none provided
        """
        if self.filenames:
            for filename in self.filenames:
                yield from self.grep_file(filename)
        else:
            yield from self.grep_stdin()

    def grep_file(self, filename):
        """
        _grep_file(self, filename)

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
        if bool(re.search(self.pattern, line)) ^ self.invertmatch:
            yield line

    def grep_stdin(self):
        for linenum, line in enumerate(self.read_stdin().splitlines()):
            for line in self.grep_line(line):
                yield GrepSuccess('<stdin>', line, linenum)

    def do(self):
        """
        do(self)

        Returns a Python representation of the output of this command

        Returns a list of GrepSuccess and GrepError objects
        """
        return self.grep_all()

    def __str__(self):
        """
        __str__(self)

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

        return '\n'.join(singlestr(arg) for arg in self.do())

def grep(pattern, *args, **options):
    """
    grep(pattern, *args, **options)

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
