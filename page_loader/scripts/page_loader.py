from page_loader.args_parser import get_args
from page_loader.page_loader_engine import download
from page_loader.internal_exceptions import PageLoaderError
import sys
import logging

logger = logging.getLogger('page_loader')


def main():
    try:
        args = get_args()
        print(download(args.url, args.output, args.verbose))
        sys.exit()
    except PageLoaderError as err:
        logger.exception(err, exc_info=False)
        sys.exit(1)


if __name__ == '__main__':
    main()
