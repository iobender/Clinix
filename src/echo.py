# echo.py
# emulates the echo tool

import clinix

class EchoCommand(clinix.ClinixCommand):
    """
    class EchoCommand(clinix.ClinixCommand)

    Class to represent an echo command
    """

    def __init__(self, args, options):
        """
        __init__(self, args, options)

        args is a list of things to output (any object is fine, not just strings)
        options is a dict of options to echo
        """

        super().__init__(options)
        self.args = args

    def _parse_options(self, options):
        """
        _parse_options(self, options)

        parses the options given to echo
        """

        pass

    def __str__(self):
        """
        __str__(self)

        Outputs each of the args given to echo, one per line,
        although each object may take up more than one line
        """

        return '\n'.join(str(arg) for arg in self.args)

def echo(*args, **options):
    """
    echo(*args, **options)

    echoes a string representation of each of its arguments, 1 per line

    options is a dict of options to echo
    Valid options (with defaults):
        
    """

    return EchoCommand(args, options)
