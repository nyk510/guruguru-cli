from typing import Union

from . import constance
from .client import guruguru_session
from .competitions import show_lb


class NotAuthenticatedError(BaseException):
    pass


def create_submission(competition: Union[str, int], file: str, skip_lb_view=False, **kwargs) -> dict:
    """
    create new submission.
    when can post submission correctly, raise ValueError.

    Args:
        competition: competition id
        file: path to submission file.
        skip_lb_view: If true, skip show LB information after submission
        **kwargs:

    Returns:
        created submission object
    """
    print('create submission')
    try:
        conf_data = constance.config.load()
    except FileNotFoundError:
        raise NotAuthenticatedError('config file does not exist. Authorization first use `guruguru auth login`.')

    username = conf_data.get('user', {}).get('username', None)
    if username is None:
        raise ValueError('username cant detected. `guruguru auth login` try again.')
    response = guruguru_session.get('/teams/', params={'competition': competition,
                                                       'engaged_in': username})

    if response.status_code != 200:
        raise ValueError(response.text)
    data = response.json()
    results = data.get('results', [])
    if len(results) == 0:
        raise ValueError(f'No team are matched. confirm to engaged into the competition (id={competition}).')
    my_team = results[0]
    my_team_id = my_team.get('id')
    files = {
        'file': open(file, 'r')
    }

    response = guruguru_session.post('/teams/submissions/', data={
        'memo': 'create from guruguru cli',
        'team': my_team_id
    }, files=files)

    if response.status_code != 201:
        raise ValueError(f'{response.status_code} {response.request} {response.headers} {response.text}')

    sub_data = response.json()
    public_score = sub_data.get('publicScore', None)
    private_score = sub_data.get('privateScore', None)

    if public_score is None and private_score is None:
        raise ValueError(f'Fail to calculate score. {response.json()}')
    print('🎉 Submission Success')
    print(f' - Public: \t{public_score:.4f}')
    if private_score:
        print(f' - Private:\t{private_score:.4f}')

    if not skip_lb_view:
        try:
            show_lb(competition=competition, private=False, n_top=10)
        except ValueError:
            pass

    return sub_data
