import argparse
from os import getcwd

def get_args():
    parser = argparse.ArgumentParser(description='Downloads WEB pages and saves to the file.')
    parser.add_argument('url', help='url of  page for downloading')
    parser.add_argument(
        '-o',
        '--output',
        default=getcwd(),
        help='sets path of saving WEB page')
    return parser.parse_args()