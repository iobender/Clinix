# grep.py
# emulates output of the grep command

import clinix
import re
from collections import namedtuple

GrepSuccess = namedtuple('GrepSuccess', 'file line linenum')
GrepError = namedtuple('GrepError', 'file reason')

class GrepOutput(clinix.ClinixOutput):
    """
    class GrepOutput(ClinixOutput)

    represents the output of the grep command
    """

    def __init__(self, result, options):
        self.result = [res for fileresult in result for res in fileresult]
        self.set_options(options)

    def set_options(self, options):
        self.linenums = options.get('n', False) or options.get('linenumber', False)
        
    def __str__(self):
        def singlestr(arg):
            if isinstance(arg, GrepSuccess):
                result = ''
                if self.linenums:
                    result += str(arg.linenum) + ':'
                result += arg.line
                return result
            elif isinstance(arg, GrepError):
                return 'grep: ' + arg.file + ': ' + arg.reason
            else:
                raise Exception("Don't know how to handle grep result " + arg.__class__.__name__)
        return '\n'.join(singlestr(arg) for arg in self.result)

def grep(pattern, *args, **options):
    """
    grep(pattern, *args, **options)

    searches the given files for the given pattern

    pattern is a regular expression interpretted by Python's re module

    options is a dict of options to grep
    Valid options (with defaults):
        
        n=False, linenumber=False:
            if True, report the line numbers of matching lines as well
    """

    regex = re.compile(pattern)
    result = [_grep_file(regex, filename) for filename in args]
    return GrepOutput(result, options)

def _grep_file(regex, filename, **options):
    results = []
    try:
        with open(filename) as file:
            for linenum, line in enumerate(file):
                line = line.rstrip()
                if re.search(regex, line):
                    results.append(GrepSuccess(filename, line, linenum))
        return results
    except IOError as e:
        return [GrepError(filename, e.strerror)]
