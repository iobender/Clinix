# clinix.py

import __main__
import sys

class ClinixCommand:
    """
    class ClinixCommand

    This class represents a command
    Creating one does not mean executing the command, so one could
    craft a certain command and save it to a variable and run it
    over and over

    Commands are created by calling them as a function, 
    with arguments passed as positional args and options passed as keyword args, e.g.

    >>> g = grep('blah.config', '^#', invertmatch=True)

    will bind g to a grep command that, when run, will print out all lines in
    'blah.config' that don't start with a #

    The command itself is actually run by calling .do() on it
    Typing a command in the REPL will also execute it, but this is
    because I have abused __repr__ here. Calling .__repr__() on a ClinixCommand
    will actually call .do() on it and cause the command to take place. I did this so
    these commands could be used effectively in the REPL. However, this means that I must 
    return empty string from __repr__ so that no additional output is produced in the REPR 
    other than the output from the command, e.g. if it prints to screen or writes to a file.

    .do() actually calls .__str__() on itself and writes the result to this command's stdout,
    whether it be sys.stdout, or a file, or possibly something else in the future. 
    So __str__ is actually when the command is evaluated, but returns a string of what should be 
    written to stdout/a file/whatever

    The goal is to be able to execute commands saved in variables multiple times, like an alias in a shell

    You can redirect stdout of a command to a file by using the > operator, with the command 
    on the left and a filename as a string on the right, e.g.

    >>> g = grep('blah.config', '^#') > 'comments.txt'

    will create the file 'comment.txt' containing all lines starting with a # in 'blah.config'

    I have attempted to emulate existing *nix-like tools as best I could, but you should refer to
    the docs for the actualy Clinix version of them for usage
    """
    
    def __init__(self, options):
        """
        __init__(self, options)

        Create a new ClinixCommand, with the given options as a dict
        Set the commands stdin, stdout, and stderr
        And call parse_options to set the command's options, which should
        be handled by the subclass that invoked this
        """
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.parse_options(options)

    def parse_options(self, options):
        """
        parse_options(self, options)

        Interprets the options dict passed as keyword args to this command
        Should throw an error if an unrecognized option is given
        """
        pass

    def __gt__(self, new_stdout):
        """
        __gt__(self, new_stdout)

        Redirects the stdout of this command to new_stdout
        New_stdout must be sys.stdout or a filename
        If it is a filename, the file will be created if it 
        does not yet exist, or overwritten if it does
        """
        self.stdout = new_stdout
        return self

    def do(self):
        """
        do(self)

        Forces execution of this command. This should be a repeatable operation.
        Writes to the proper output channel as well
        calls __str__ on itself to determine what to write
        """
        if isinstance(self.stdout, str):
            outfile = open(self.stdout, 'w') # TODO: close
        elif self.stdout == sys.stdout:
            outfile = self.stdout
        else:
            raise Exception("Can't write to " + self.stdout)
        output = str(self) + '\n'
        outfile.write(output)

    def __repr__(self):
        """
        __repr__(self)

        Forces execution of this command, and returns empty string
        (yes I know this is abuse of __repr__ but that's what it took
        to make this work in the REPL and in programs)
        """
        self.do()
        return ''

