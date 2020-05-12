from urllib.parse import urljoin

import pytest
import responses

from guruguru.competitions import show_lb
from .conftest import MOCK_API_URL


@responses.activate
def test_show_lb():
    responses.add('GET', url=urljoin(MOCK_API_URL, '/competitions/1/public/'), json={
        'results': [
            {'name': 'kamitu', 'totalSubmissions': 3, 'bestPublicScore': .5,
             'lastSubmittedAt': '2019-01-01T12:00:00+09:00'},
            { 'name': 'nyk', 'lastSubmittedAt': None }
        ]
    }, status=200)
    show_lb(competition=1, )


@responses.activate
def test_show_lb_competiton_id_is_404_not_found():
    responses.add('GET', url=urljoin(MOCK_API_URL, '/competitions/2/public/'),
                  json={'detail': '見つかりませんでした'}, status=404)

    with pytest.raises(ValueError):
        show_lb(2)
