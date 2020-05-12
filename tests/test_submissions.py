from urllib.parse import urljoin

import pandas as pd
import pytest
import responses

from guruguru.submissions import create_submission, NotAuthenticatedError
from .conftest import MOCK_API_URL


@pytest.fixture
def submission_path(tmpdir) -> str:
    p = tmpdir.join('submission.csv')
    df = pd.DataFrame([[1, 2, 3]], index=['target']).T
    df.to_csv(p, index=False)
    return p


def test_not_authorized(submission_path):
    with pytest.raises(NotAuthenticatedError):
        create_submission(1, file=submission_path)


def test_no_username_in_token(monkeypatch, submission_path):
    monkeypatch.setattr('guruguru.constance.config.load', lambda: {'foo': 'bar'})
    with pytest.raises(ValueError):
        create_submission(1, file=submission_path)


@responses.activate
@pytest.mark.usefixtures('authorized')
def test_fail_to_fetch_teams(submission_path):
    responses.add(responses.GET, url=urljoin(MOCK_API_URL, '/teams/'), json={}, status=404)
    with pytest.raises(ValueError):
        create_submission(1, file=submission_path)


@responses.activate
@pytest.mark.usefixtures('authorized')
def test_fail_to_fetch_my_tea(submission_path):
    # request success but no teams are matched
    responses.add(responses.GET, url=urljoin(MOCK_API_URL, '/teams/'), json={
        'results': []
    }, status=200)
    with pytest.raises(ValueError):
        create_submission(1, file=submission_path)


@responses.activate
@pytest.mark.usefixtures('authorized')
def test_can_submit_by_fail_to_calculation(submission_path):
    responses.add(responses.GET, url=urljoin(MOCK_API_URL, '/teams/'), json={
        'results': [
            {'id': 128}
        ]
    }, status=200)

    responses.add(responses.POST, url=urljoin(MOCK_API_URL, '/teams/submissions/'), json={
        'id': '12345',
        'succeeded': False
    }, status=201)

    with pytest.raises(ValueError):
        create_submission(1, file=submission_path)


@responses.activate
@pytest.mark.usefixtures('authorized')
def test_can_submit_by_fail_to_calculation(submission_path, monkeypatch):
    responses.add(responses.GET, url=urljoin(MOCK_API_URL, '/teams/'), json={
        'results': [
            {'id': 128}
        ]
    }, status=200)

    responses.add(responses.POST, url=urljoin(MOCK_API_URL, '/teams/submissions/'), json={
        'id': '12345',
        'privateScore': .7,
        'publicScore': .8
    }, status=201)

    def silent(*args, **kwargs):
        return None

    monkeypatch.setattr('guruguru.submissions.show_lb', silent)
    create_submission(1, file=submission_path)
