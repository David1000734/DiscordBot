"""
This module will contain all custom exceptions. The purpose of these
exception is to be used in try except cases where it would be
preferable to raise one of these to improve readability.
"""

class UnknownCommand(Exception):
    """
    Exception raised for commands that exceed the maxium neccessary
    words for the command. Message is not required.
    """

    def __init__(self, message = None):
        self.message = message
        super().__init__(self.message)
# UnknownCommand, END

class InvalidSubreddit(Exception):
    """
    Exception raised for subreddits that are caught during the
    main reddit command for being incorrectly formatted.
    (No subreddits should contain a space). Message is not required
    """

    def __init__(self, message = None):
        self.message = message
        super().__init__(self.message)
# InvalidSubreddit, END
