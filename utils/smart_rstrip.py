"""Right strips string"""


def smart_rstrip(string, char):
    """Right strips string from first occurrence from given char"""

    try:
        idx = string.index(char)
        string = string[:idx]
        return string
    except ValueError:
        return string
