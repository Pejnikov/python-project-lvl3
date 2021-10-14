import requests
from re import sub
from os.path import isdir, join


def get_page_content(url: str) -> str:
    responce = requests.get(url)
    return responce.text


def make_file_name(url: str) -> str:
    name_items = []
    url_without_schema = sub(r'^https?:\/\/', '', url)
    for symbol in url_without_schema:
        if symbol.isalpha() or symbol.isdigit():
            name_items.append(symbol)
        else:
            name_items.append('-')
    name_items.append('.html')
    return ''.join(name_items)


def save_content(path: str, name: str, content: str) -> str:
    if not isdir(path):
        raise ValueError("Directory doesn't exist")
    file_path = join(path, name)
    with open(file_path, 'w') as page_file:
        page_file.write(content)
    return file_path


def download(url: str, download_path: str) -> str:
    page_content = get_page_content(url)
    file_name = make_file_name(url)
    downloaded_file_path = save_content(download_path, file_name, page_content)
    return downloaded_file_path
