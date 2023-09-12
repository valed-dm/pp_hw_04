"""User input"""


import sys


def user_input():
    """User input"""

    wks = None
    rtd = None
    if "-w" not in sys.argv:
        try:
            wks = int(input("enter workers qty [1-4], default=1:_"))
        except ValueError:
            pass
    if "-r" not in sys.argv:
        rtd = input("enter doc root dir, default=DOCUMENT_ROOT:_")

    return wks, rtd
