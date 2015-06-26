# clinix.py

import __main__
import sys
from collections import namedtuple

InputType = namedtuple('InputType', 'type source')

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
    the docs for the actual Clinix version of them for usage
    """
    
    def __init__(self, options):
        """
        __init__(self, options)

        Create a new ClinixCommand, with the given options as a dict
        Set the commands stdin, stdout, and stderr
        And call _parse_options to set the command's options, which should
        be handled by the subclass that invoked this
        """

        self.stdin = InputType('stdin', sys.stdin)
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self._parse_options(options)

    def parse_options(self, options):
        """
        _parse_options(self, options)

        Interprets the options dict passed as keyword args to this command
        Should throw an error if an unrecognized option is given
        """

        pass

    def __gt__(self, new_stdout):
        """
        __gt__(self, new_stdout)

        >>> comm() > 'file.txt'

        Redirects the stdout of this command to new_stdout
        new_stdout must be sys.stdout or a filename
        If it is a filename, the file will be created if it 
        does not yet exist, or overwritten if it does

        Returns this command
        """

        self.stdout = new_stdout
        self.overwrite_stdout = True
        return self

    def __ge__(self, new_stdout):
        """
        __ge__(self, new_stdout)

        >>> comm() >= 'file.txt'

        Redirects the stdout of this command to new_stdout
        new_stdout must be sys.stdout or a filename
        If it is a filename, the file will be appended to, and
        created if it does not exist

        Returns this command

        Note that this syntax differs from most shells as it uses >= 
        for appending to a file and not >>
        This is because >> and > have different precedent levels 
        (and more significantly | has a precedence level in between them)
        but >= and > have the same precedence.
        """

        self.stdout = new_stdout
        self.overwrite_stdout = False
        return self

    def __lt__(self, source):
        """
        __lt__(self, source)

        comm() < 'input.txt'

        Sets source to be this commands stdin. source should be a filename
        The file will not be opened and read until the command is evaluated
        """

        self.stdin = InputType('file', source)
        return self

    def __or__(self, source):
        """
        __or__(self, source)

        Only implemented because Python won't call __ror__ if two operands are of the same type
        All the logic occurs in __ror__
        """

        return source.__ror__(self)

    def __ror__(self, source):
        """
        __ror__(self, source)

        Implements piping of commands. When comm1 is piped to comm2 like:

        >>> comm1() | comm2() 

        Then comm2's __ror__ is invoked (ClinixCommands should not implement __or__)
        The input source of comm2 is set to be comm1, and comm2 is returned. 

        Other types can also be piped to ClinixCommands (provided they don't implement __or__,
        because if they do they will steal the operator for themselves)

        >>> x | comm()

        x will be translated into a string as evaluation time and treated as stdin
        """

        self.stdin = InputType('pipe', source)
        return self

    def read_stdin(self):
        """
        read_stdin(self)

        Gets the value of this commands stdin
        If it is actually stdin, just reads from stdin
        If we have been piped to, call str on the input source and use those lines
            (if a list was piped to use, call str on its elements and join with newlines)
        """

        if self.stdin.type == 'stdin':
            return self.stdin.source.read()
        elif self.stdin.type == 'file':
            try:
                with open(self.stdin.source) as infile:
                    return infile.read()
            except IOError as e:
                raise Exception('Error reading file ' + infile + ': ' + e.strerror)
        elif self.stdin.type == 'pipe':
            source = self.stdin.source
            if isinstance(source, list) and not isinstance(source, str):
                source = '\n'.join(source)
            return str(source)
        else:
            raise Exception('Unknown stdin type: ' + self.stdin.type)

    def do(self):
        """
        do(self)

        Forces execution of this command. This should be a repeatable operation.
        Writes to the proper output channel as well
        calls __str__ on itself to determine what to write
        """

        if isinstance(self.stdout, str):
            mode = 'w' if self.overwrite_stdout else 'a'
            outfile = open(self.stdout, mode) # TODO: close
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

