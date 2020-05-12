from urllib.parse import urljoin

import pytest
import responses

from guruguru.authentication import request_login, login
from .conftest import MOCK_API_URL


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as res:
        res.add(responses.POST, urljoin(MOCK_API_URL, '/auth/login/'), json={'status': 'ok'}, status=200)
        yield res


@pytest.fixture
def increment_getpass(monkeypatch):
    monkeypatch.setattr('guruguru.authentication.getpass', lambda x: 'hogehoge')


@pytest.mark.usefixtures('mocked_responses', 'increment_getpass')
def test_post_authorization():
    res = request_login(username='nyk', password='510')
    assert res == {'status': 'ok'}


@responses.activate
def test_fail_authorization():
    responses.add(responses.POST, urljoin(MOCK_API_URL, '/auth/login/'), status=401)
    with pytest.raises(ValueError):
        request_login(username='nyk', password='510')


@responses.activate
@pytest.mark.usefixtures('increment_getpass')
def test_success_login(monkeypatch, capsys):
    responses.add(responses.POST, urljoin(MOCK_API_URL, '/auth/login/'), status=200, json={'status': 'ok'})
    monkeypatch.setattr('builtins.input', lambda x: 'foo')

    login()
    captured = capsys.readouterr()
    assert captured.out.split('\n')[-2] == 'Login Success!'


@responses.activate
@pytest.mark.usefixtures('increment_getpass')
def test_fail_login(monkeypatch, capsys):
    responses.add(responses.POST, urljoin(MOCK_API_URL, '/auth/login/'), status=401)
    monkeypatch.setattr('builtins.input', lambda x: 'foo')

    login()
    captured = capsys.readouterr()
    assert captured.out.split('\n')[-2] == 'Too Many Time Mistakes'
