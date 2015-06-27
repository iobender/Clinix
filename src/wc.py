# wc.py
# emulates the wc program

import clinix
from collections import namedtuple

WcSuccess = namedtuple('WcSuccess', 'file lines words bytes')
WcError = namedtuple('WcError', 'file reason')

class WcCommand(clinix.ClinixCommand):
    """
    Class to represent a wc command
    """

    def __init__(self, args, options):
        """
        args is a list of files to count from
        options is a list of options to wc
        """

        super().__init__(options)
        self.filenames = args

    def parse_options(self, options):
        """
        parses the options given to wc
        """

        self.count_lines = options.get('lines', False) or options.get('l', False)
        self.count_words = options.get('words', False) or options.get('w', False)
        self.count_bytes = options.get('bytes', False) or options.get('c', False)

        # by default, count lines, words, and bytes, overridden if something specific is passed
        if not any((self.count_lines, self.count_words, self.count_bytes)):
            self.count_lines = True
            self.count_words = True
            self.count_bytes = True

    def wc_one(self, filename):
        """
        counts for a single file

        returns either WcSuccess or WcError
        """

        try:
            with open(filename) as f:
                n_lines, n_words, n_bytes = self.wc_text(f.read())
                return WcSuccess(filename, n_lines, n_words, n_bytes)
        except IOError as e:
            return WcError(filename, e.strerror)

    def wc_text(self, text):
        """
        Counts the lines, words, and bytes of a string
        """

        n_lines = len(text.splitlines())
        n_words = len(text.split())
        n_bytes = len(text)
        return n_lines, n_words, n_bytes

    def wc_stdin(self):
        """
        Reads stdin and returns the lines, words, and bytes
        """

        return WcSuccess('', *self.wc_text(self.read_stdin()))

    def total(self, results):
        """
        Totals up the lines, words, and bytes from a list of 
        results
        """

        total_lines = 0
        total_words = 0
        total_bytes = 0
        for result in results:
            if isinstance(result, WcSuccess):
                total_lines += result.lines
                total_words += result.words
                total_bytes += result.bytes
        return WcSuccess('total', total_lines, total_words, total_bytes)

    def eval(self):
        """
        returns a Python representation of the result of this command;w
        """

        filenames = list(clinix.expand_files(self.filenames))
        if filenames:
            return [self.wc_one(f) for f in filenames]
        else:
            return [self.wc_stdin()]
    
    def __str__(self):
        """
        Outputs each of the totals and filenames

        If more than one file given, output total as well
        """

        # TODO: format vertically aligned
        def singlestr(arg):
            if isinstance(arg, WcSuccess):
                return '{} {} {} {}'.format(
                    arg.lines if self.count_lines else '',
                    arg.words if self.count_words else '',
                    arg.bytes if self.count_bytes else '',
                    arg.file
                )
            elif isinstance(arg, WcError):
                return arg.file + ': ' + arg.reason
            else:
                raise Exception("Don't know how to handle wc result " + arg.__class__.__name__)

        results = self.eval()
        if len(results) != 1:
            results.append(self.total(results))
        return '\n'.join(singlestr(arg) for arg in results)

def wc(*args, **options):
    """
    counts the number of lines, words, and bytes in the given files
    """

    return WcCommand(args, options)

