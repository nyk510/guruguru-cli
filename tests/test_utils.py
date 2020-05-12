import pytest
from freezegun import freeze_time

from guruguru.utils import to_upper_int, pretty_date


@pytest.mark.parametrize('x, expect', [
    (1, 1),
    (.5, 1),
    (0, 0),
    (50, 50),
    (10.1, 11)
])
def test_upper_int(x, expect):
    assert to_upper_int(x) == expect


@pytest.mark.parametrize('x, expect', [
    (None, ''),
    ('', ''),
    ('2019-12-31T12:01:00+09:00', ''),
    ('2019-12-31T11:59:51+09:00', 'just now'),
    ('2019-12-31T11:59:50+09:00', '10 seconds ago'),
    ('2019-12-31T11:59:10+09:00', '50 seconds ago'),
    ('2019-12-31T11:59:00+09:00', 'a minute ago'),
    ('2019-12-31T11:00:00+09:00', 'a hour ago'),
    ('2019-12-31T10:50:00+09:00', 'a hour ago'),
    ('2019-12-31T10:00:00+09:00', '2 hours ago'),
    ('2019-12-30T12:00:00+09:00', 'yesterday'),
    ('2019-12-29T13:00:00+09:00', 'yesterday'),
    ('2019-12-29T12:00:00+09:00', '2 days ago'),
    ('2019-12-24T13:00:00+09:00', '6 days ago'),
    ('2019-12-24T12:00:00+09:00', '1 week ago'),
    ('2019-12-01T13:00:00+09:00', '5 weeks ago'),
    ('2019-11-30T13:00:00+09:00', '1 month ago'),
    ('2019-10-31T13:00:00+09:00', '1 month ago'),
    ('2019-10-31T12:00:00+09:00', '2 months ago'),
    ('2018-12-31T13:00:00+09:00', '11 months ago'),
    ('2018-12-31T12:00:00+09:00', '1 year ago'),
])
def test_pretty_time(x, expect, now):
    with freeze_time(now):
        assert pretty_date(x) == expect


@pytest.mark.parametrize('x, expect', [
    ('2019-12-31T12:01:00+09:00', ''),
    ('2019-12-30T12:01:00+09:00', 0),
    ('2019-12-30T12:00:00+09:00', 1),
    ('2019-12-29T11:01:00+09:00', 2),
])
def test_pretty_time_as_days(x, expect, now):
    with freeze_time(now):
        assert pretty_date(x, as_days=True) == expect
