from page_loader.args_parser import get_args
from page_loader.page_loader_engine import download


def main():
    args = get_args()
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
