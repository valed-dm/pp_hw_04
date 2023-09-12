"""Converts now to RFC 1123 format"""


from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time


def time_now_rfc_1123() -> str:
    """Makes now in RFC 1123 format"""

    now = datetime.now()
    stamp = mktime(now.timetuple())
    res = format_date_time(stamp)

    return res
