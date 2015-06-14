# clinix.py

class ClinixOutput:
    """
    class ClinixOutput

    Class to represent the output of a single clinix command
    """

    def __init__(self):
        pass

    def stdout(self):
        return str(self).splitlines()

    def __repr__(self):
        return self.__class__.__name__ + '\n' + str(self)
