from datetime import datetime

import numpy as np
import pandas as pd
from dateutil import parser
from dateutil.relativedelta import relativedelta


def to_upper_int(x: float, epsilon=1e-7) -> int:
    x = float(x) - epsilon
    return int(np.floor(x) + 1)


def convert_to_timezone_naive(time):
    """
    Converts a potentially timezone-aware datetime to be a naive UTC datetime
    """
    if time.tzinfo:
        time -= time.utcoffset()
        time = time.replace(tzinfo=None)
    return time


def pretty_date(time=None, as_days=False) -> str:
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    if time is None or pd.isnull(time):
        return ''

    now = datetime.now()
    if isinstance(time, str):
        if len(time) == 0: return ''
        time = parser.parse(time)
    elif isinstance(time, int):
        time = datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        time = time
    elif not time:
        time = now
    else:
        return ''

    time = convert_to_timezone_naive(time)
    if now < time:
        return ''
    diff = relativedelta(now, time)

    day_diff = diff.days
    month_diff = diff.months
    year_diff = diff.years
    hour_diff = diff.hours
    minute_diff = diff.minutes
    second_diff = diff.seconds

    if as_days:
        return day_diff

    if year_diff > 1:
        return f'{year_diff} years ago'
    if year_diff > 0:
        return '1 year ago'

    if month_diff > 1:
        return f'{month_diff} months ago'
    if month_diff > 0:
        return '1 month ago'

    if day_diff > 13:
        return f'{to_upper_int(day_diff / 7)} weeks ago'
    if day_diff > 6:
        return '1 week ago'
    if day_diff > 1:
        return f'{day_diff} days ago'
    if day_diff == 1:
        return 'yesterday'

    if hour_diff > 1:
        return f'{hour_diff} hours ago'
    if hour_diff > 0:
        return 'a hour ago'

    if minute_diff > 1:
        return f'{minute_diff} minutes ago'
    if minute_diff > 0:
        return 'a minute ago'

    if second_diff > 9:
        return f'{second_diff} seconds ago'
    return 'just now'
