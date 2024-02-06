"""
The program checks, whether the package version is present in the pypi repository, using unpatched simple API

By default, the exit code = 1 when not found, or 0 when found. Change it using -X, or -E options.

Call without parameters to get help, or use --help option.
"""

import argparse
import sys
from html import parser
from urllib import parse as url_parse, request


__version__ = '0.0.3'

__all__ = [
    '__version__',
    'main',
]


class VersionAction(argparse.Action):
    """Print the version as an action"""
    def __init__(
        self,
        option_strings,
        dest=argparse.SUPPRESS,
        default=argparse.SUPPRESS,
        help=None
    ):
        """Constructor"""
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        print(__version__)
        sys.exit(0)


def main(argv=None):
    """A main procedure"""
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(
        prog=argv[0],
        description=__doc__,
        formatter_class=type('Formatter', (
            argparse.RawTextHelpFormatter,
            argparse.MetavarTypeHelpFormatter
        ), {})
    )
    parser.add_argument(
        '--version',
        help='show package version and exit',
        action=VersionAction
    )
    parser.add_argument(
        dest='package_name',
        type=str,
        help='Package name to be checked, use `python setup.py --name` in the package root',
    )
    parser.add_argument(
        dest='version',
        type=str,
        help='Version to be checked, use `python setup.py --version` in the package root',
    )

    parser.add_argument(
        '-R', '--repo', '--repository',
        dest='repository',
        type=str,
        default='https://pypi.org',
        help='Repository site, %(default)s by default',
    )

    parser.add_argument(
        '-U', '--user', '--username',
        dest='username',
        type=str,
        default=None,
        help='Repository username if necessary',
    )

    parser.add_argument(
        '-P', '--pass', '--passwd', '--password',
        dest='password',
        type=str,
        default=None,
        help='Repository password if necessary',
    )

    parser.add_argument(
        '-E', '--avoid-exit-code',
        dest='avoid',
        action='store_true',
        default=False,
        help='If you would like to avoid generating specific exit code',
    )

    parser.add_argument(
        '-X', '--revert-exit-code',
        dest='revert',
        action='store_true',
        default=False,
        help='If you would like to revert exit code having code=1 when the version found',
    )

    parser.add_argument(
        '-T', '--text-output',
        dest='text',
        action='store_true',
        default=False,
        help='If you would like to output the result to the stdout, as TRUE when found, or FALSE if not found',
    )

    if len(argv) <= 1:
        parser.print_help()
        return
    options = parser.parse_args(argv[1:])
    p = PackageHandler(options)
    auth = request.HTTPBasicAuthHandler(request.HTTPPasswordMgrWithDefaultRealm())
    auth.add_password(realm=None, uri=options.repository, user=options.username, passwd=options.password)
    opener = request.build_opener(auth)
    content = opener.open(
        url_parse.urljoin(options.repository, '/simple/%s/' % options.package_name)
    ).read().decode('utf8')
    p.feed(content)

    if options.text:
        print('TRUE' if p.found else 'FALSE')
    if options.avoid:
        return 0
    if p.found:
        return 1 if options.revert else 0
    return 0 if options.revert else 1


class PackageHandler(parser.HTMLParser):
    """Handler to find the package reference"""
    found = False

    def __init__(self, options):
        """Constructor"""
        super().__init__()
        self.options = options

    def handle_starttag(self, tag, attrs):
        """Handles tag to find a reference to the package"""
        if tag == 'a':
            named = dict([pair if len(pair) == 2 else (pair, None) for pair in attrs])
            if 'href' in named:
                if '/%s-%s.' % (self.options.package_name, self.options.version) in named['href']:
                    self.found = True


if __name__ == '__main__':
    sys.exit(main(sys.argv))
