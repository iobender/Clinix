# echo.py
# emulates the echo tool

import clinix

class EchoOutput(clinix.ClinixOutput):
    """
    class EchoOutput(ClinixOutput)

    represents output from echo
    """
    def __init__(self, output):
        self.output = output

    def __str__(self):
        return self.output

def echo(*args, **options):
    """
    echo(*args, **options)

    echoes a string representation of each of its arguments, 1 per line

    options is a dict of options to echo
    Valid options (with defaults):
        
    """
    result = '\n'.join(map(str, args))
    return EchoOutput(result)
