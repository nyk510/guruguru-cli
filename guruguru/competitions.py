from typing import Union

import pandas as pd
from tabulate import tabulate

from .client import guruguru_session
from .utils import pretty_date


def to_relative_string(date_str: str) -> Union[str, None]:
    """
    convert time aware datetime string to relative time-diff string from now
    If cant parse or some error, return None

    Args:
        date_str: target date string.

    Returns:
        pretty time-diff string (human readable)
    """
    try:
        x = pd.to_datetime(date_str)
        x = x.tz_convert(None)
        return pretty_date(x)
    except Exception as e:
        return None


def show_lb(competition: Union[str, int],
            private=False, n_top: Union[int, None] = None, **kwargs) -> pd.DataFrame:
    """
    fetch leader board and print to console as pretty table

    Args:
        competition: competition id
        private: If true, fetch private lb.
        n_top: maximum number of teams to show
        **kwargs:

    Returns:
        leader board dataframe
    """
    name = 'private' if private else 'public'

    response = guruguru_session.get(f'/competitions/{competition}/{name}/')
    if response.status_code != 200:
        raise ValueError(f'competition {competition} is not found. ')

    teams = response.json().get('results', [])
    lb_df = pd.DataFrame(teams)

    vis_df = lb_df.copy()
    if n_top is not None and len(vis_df) > n_top:
        vis_df = vis_df.head(n_top)

    if private:
        use_columns = ['name', 'privateRank', 'bestPrivateScore', 'bestPublicScore', 'lastSubmittedAt',
                       'totalSubmissions']
    else:
        use_columns = ['name', 'bestPublicScore', 'lastSubmittedAt', 'totalSubmissions', ]

    vis_df = vis_df[use_columns]

    for c in ['lastSubmittedAt']:
        vis_df[c] = vis_df[c].map(to_relative_string)

    print(tabulate(vis_df.fillna('----'), headers='keys', tablefmt='github', showindex=False))
    return lb_df
