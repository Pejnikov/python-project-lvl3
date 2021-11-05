import argparse
from os import getcwd
from page_loader.logger import DEF_LOG_LEVEL


def get_args():
    parser = argparse.ArgumentParser(
        description='Download WEB pages and save to the file.'
    )
    parser.add_argument('url', help='URL of  page for downloading')
    parser.add_argument(
        '-o',
        '--output',
        default=getcwd(),
        help='Set path of saving WEB page')
    parser.add_argument(
        '--verbose',
        '-v', action='count',
        default=DEF_LOG_LEVEL,
        help='Increase the verbosity of logs: "-v" for warning, "-vv" for info \
            and "-vvv" for debug')
    return parser.parse_args()
