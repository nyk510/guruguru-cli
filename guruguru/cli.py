"""
Guruguru Cli Entrypoint.
"""
from . import authentication
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def main():
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')
    parse_authentication(subparsers)
    args = parser.parse_args()
    func = args.func

    kwrgs = dict(vars(args))
    print(kwrgs)
    del kwrgs['func']
    del kwrgs['command']

    func(**kwrgs)


def parse_authentication(subparsers):
    parser_auth = subparsers.add_parser('auth', help='authentication')
    subparsers_auth = parser_auth.add_subparsers(dest='command')
    subparsers_auth.required = True
    subparsers_auth.choices = ['login']

    parser_auth_login = subparsers_auth.add_parser('login',
                                                   formatter_class=ArgumentDefaultsHelpFormatter)
    parser_auth_login.set_defaults(func=authentication.login)
