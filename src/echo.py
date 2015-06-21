# echo.py
# emulates the echo tool

import clinix

class EchoCommand(clinix.ClinixCommand):

    def __init__(self, args, options):
        super().__init__(options)
        self.args = args

    def parse_options(self, options):
        pass

    def __str__(self):
        return '\n'.join(str(arg) for arg in self.args)

def echo(*args, **options):
    """
    echo(*args, **options)

    echoes a string representation of each of its arguments, 1 per line

    options is a dict of options to echo
    Valid options (with defaults):
        
    """
    return EchoCommand(args, options)
