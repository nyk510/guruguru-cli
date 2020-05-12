import os

import pytest
from dateutil.parser import parse

pytest_plugins = 'pytester'

MOCK_API_URL = 'http://api.guruguru-mockup.com'
os.environ.setdefault('GURUGURU_BASE_URL', MOCK_API_URL)


@pytest.fixture()
def now():
    """create 2019/12/31 12:00 at Tokyo (+9 Hours)"""
    return parse('2019-12-31T12:00:00+09:00')


@pytest.fixture(autouse=True, scope='function')
def setup(monkeypatch, tmpdir):
    monkeypatch.setenv('GURUGURU_BASE_URL', MOCK_API_URL)
    monkeypatch.setattr('guruguru.client.guruguru_session.base_url', MOCK_API_URL)
    monkeypatch.setattr('guruguru.constance.config_dir', tmpdir)


@pytest.fixture()
def authorized(monkeypatch):
    token = {
        'user': {
            'username': 'nyk510'
        },
        'token': '123456789'
    }
    monkeypatch.setattr('guruguru.constance.config.load', lambda: token)
