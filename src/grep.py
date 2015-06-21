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
        super().__init__(options)
        self.compile_pattern(pattern)
        self.filenames = args

    def parse_options(self, options):
        self.ignorecase = options.get('i', False) or options.get('ignorecase', False)
        self.linenumber = options.get('n', False) or options.get('linenumber', False)

    def compile_pattern(self, pattern):
        flags = 0
        if self.ignorecase:
            flags |= re.IGNORECASE
        self.pattern = re.compile(pattern, flags)

    def grep_all(self):
        for filename in self.filenames:
            yield from self.grep_file(filename)

    def grep_file(self, filename):
        try:
            with open(filename) as file:
                for linenum, line in enumerate(file, 1):
                    line = line.rstrip()
                    if re.search(self.pattern, line):
                        yield GrepSuccess(filename, line, linenum)
        except IOError as e:
            yield GrepError(filename, e.strerror)

    def __str__(self):
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

        result = self.grep_all()
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
