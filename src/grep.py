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
        self._compile_pattern(pattern)
        self.filenames = args

    def _parse_options(self, options):
        """
        _parse_options(self, options)

        processes options to grep
        valid options are i, ignorecase, n, and linenumber
        """

        self.ignorecase = options.get('i', False) or options.get('ignorecase', False)
        self.linenumber = options.get('n', False) or options.get('linenumber', False)

    def _compile_pattern(self, pattern):
        """
        _compile_pattern(self, pattern)

        compiles the given regex pattern, considering the options given
        """

        flags = 0
        if self.ignorecase:
            flags |= re.IGNORECASE
        self.pattern = re.compile(pattern, flags)

    def _grep_all(self):
        """
        _grep_all(self)

        yields each match from each file provided
        """
        for filename in self.filenames:
            yield from self._grep_file(filename)

    def _grep_file(self, filename):
        """

        _grep_file(self, filename)
        tries to open filename, and yields all matching lines
        with some info about the lines
        if the file couldn't be opened, returns an error
        """
        try:
            with open(filename) as file:
                for linenum, line in enumerate(file, 1): # count line numbers from 1
                    line = line.rstrip() # remove trailing newline
                    if re.search(self.pattern, line):
                        yield GrepSuccess(filename, line, linenum)
        except IOError as e:
            yield GrepError(filename, e.strerror)

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

        result = self._grep_all()
        return '\n'.join(singlestr(arg) for arg in result)

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
    """

    return GrepCommand(pattern, args, options)
