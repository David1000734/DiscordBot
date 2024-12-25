# This file should be removed. Just nice little thing to have at the time

# import system module
import sys


# check if virtual environment is active or not
def is_virtualenv():
    return hasattr(sys, 'real_prefix') \
        or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)


if is_virtualenv():
    print("Running inside a virtual environment.")
else:
    print("Not running inside a virtual environment.")
