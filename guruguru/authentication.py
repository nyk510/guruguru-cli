from getpass import getpass

from .client import guruguru_session
from .constance import config


def request_login(username, password):
    response = guruguru_session.post('auth/login/', data={'username': username, 'password': password}, use_auth=False)
    if response.status_code != 200:
        raise ValueError(response.text)

    return response.json()


def login():
    n_tries = 3
    print('Login To Guruguru')
    username = input('username or email: ')
    while n_tries > 0:
        try:
            password = getpass('password: ')
            response = request_login(username, password)
            print('Login Success!')
            config.save(response)
            return
        except ValueError as e:
            print(f'[Failed] {e}\tTry Again.')
            n_tries -= 1

    print('Too Many Time Mistakes')
