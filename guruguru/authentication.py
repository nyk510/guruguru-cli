from getpass import getpass
import requests
from .constance import config
from .client import guruguru_session


def request_login():
    print('Login To Guruguru')

    username = input('username or email: ')
    password = getpass('password: ')
    print(username, password)

    response = guruguru_session.post('auth/login/', data={'username': username, 'password': password})
    if response.status_code != 200:
        raise ValueError(response.text)

    return response.json()


def login():
    n_tries = 3

    while n_tries > 0:
        try:
            response = request_login()
            config.save(response)
            return
        except ValueError as e:
            print(f'[Failed] {e}')
            n_tries -= 1

    print('Too Many Time Mistakes')
  