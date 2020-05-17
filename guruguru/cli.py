"""
Guruguru Cli Entrypoint.
"""
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from . import authentication, competitions, submissions, version


def main():
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('--version', action='store_true', help='show guruguru version')

    subparsers = parser.add_subparsers(dest='command')
    parse_authentication(subparsers)
    parse_competition(subparsers)
    parse_create_submission(subparsers)
    args = parser.parse_args()

    if args.version:
        print(version.__version__)
        return
    else:
        del args.version

    if hasattr(args, 'handler'):
        handler = args.handler
    else:
        parser.print_help()
        return

    kwrgs = dict(vars(args))
    del kwrgs['handler']
    del kwrgs['command']

    handler(**kwrgs)


def parse_authentication(subparsers):
    """add auth parser module to `subparsers`"""
    parser_auth = subparsers.add_parser('auth', help='use authentication modules.')
    subparsers_auth = parser_auth.add_subparsers(dest='command')
    subparsers_auth.required = True
    subparsers_auth.choices = ['login']

    parser_auth_login = subparsers_auth.add_parser('login',
                                                   formatter_class=ArgumentDefaultsHelpFormatter)
    parser_auth_login.set_defaults(handler=authentication.login)


def parse_create_submission(subparsers):
    parser_submission = subparsers.add_parser('submit', help='create submission')
    subparsers_submission = parser_submission.add_subparsers(dest='command')

    subparsers_submission.choices = ['create']
    parser_submission_create = subparsers_submission.add_parser('create',
                                                                help='Create New Submission from file',
                                                                formatter_class=ArgumentDefaultsHelpFormatter)
    parser_submission_create.add_argument('-c', '--competition', help='Competition to submit', required=True)
    parser_submission_create.add_argument('--file', help='Path to submission file.', required=True)
    parser_submission_create.set_defaults(handler=submissions.create_submission)


def parse_competition(subparsers):
    parser_compe = subparsers.add_parser('competition', help='show competition information')
    subparsers_compe = parser_compe.add_subparsers(dest='command')

    subparsers_compe.choices = ['lb']

    parser_competition_lb = subparsers_compe.add_parser(
        'lb',
        help='Show Leader Board',
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser_competition_lb.add_argument('-c', '--competition', help='Competition Id show LB', required=True)
    parser_competition_lb.add_argument('--private', action='store_true', help='fetch private lb')
    parser_competition_lb.add_argument('--n_top', type=int, help='maximum number of teams to show.', default=20)
    parser_competition_lb.set_defaults(handler=competitions.show_lb)
