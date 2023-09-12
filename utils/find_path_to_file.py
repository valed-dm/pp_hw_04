"""Searches for file in root dir"""


import fnmatch
import os


def find_path(directory, pattern):
    """Provides relative path to file in root dir"""

    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                return filename
