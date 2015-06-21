# clinix.py

import __main__
import sys

class ClinixCommand:
    
    def __init__(self, options):
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.parse_options(options)

    def parse_options(self, options):
        pass

    def __repr__(self):
        self.do()
        return ''

    def __gt__(self, other):
        self.stdout = other
        return self

    def do(self):
        if isinstance(self.stdout, str):
            outfile = open(self.stdout, 'w') # TODO: close
        elif self.stdout == sys.stdout:
            outfile = self.stdout
        else:
            raise Exception("Can't write to " + self.stdout)
        output = str(self) + '\n'
        outfile.write(output)
