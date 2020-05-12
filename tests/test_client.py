from guruguru.client import BaseUrlSession


def test_get_auth_headers(monkeypatch):
    monkeypatch.setattr('guruguru.client.constance.config.get_token', lambda: 'foo')
    session = BaseUrlSession(base_url=None)
    heasers = session.get_auth_headers()

    assert heasers == {'authorization': 'JWT foo'}
