# echo.py
# emulates the echo tool

import clinix

class EchoCommand(clinix.ClinixCommand):
    """
    Class to represent an echo command
    """

    def __init__(self, args, options):
        """
        args is a list of things to output (any object is fine, not just strings)
        options is a dict of options to echo
        """

        super().__init__(options)
        self.args = args

    def parse_options(self, options):
        """
        parses the options given to echo
        """

        pass

    def eval(self):
        """
        returns a Python representation of the result of this command

        for echo, just return's its arguments
        """
        return self.args

    def __str__(self):
        """
        Outputs each of the args given to echo, one per line,

        although each object may take up more than one line
        """

        return '\n'.join(str(arg) for arg in self.eval())

def echo(*args, **options):
    """
    echoes a string representation of each of its arguments, 1 per line

    options is a dict of options to echo
    Valid options (with defaults):
        
    """

    return EchoCommand(args, options)
