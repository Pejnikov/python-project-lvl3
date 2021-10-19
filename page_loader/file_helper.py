from os.path import isdir, join
from re import sub


def get_name_from_url(url: str) -> str:
    name_items = []
    url_without_schema = sub(r'^https?:\/\/', '', url)
    for symbol in url_without_schema:
        if symbol.isalpha() or symbol.isdigit():
            name_items.append(symbol)
        else:
            name_items.append('-')
    return ''.join(name_items)


def save_page_text(path: str, name: str, content: str) -> str:
    if not isdir(path):
        raise ValueError("Directory doesn't exist")
    file_path = join(path, name)
    with open(file_path, 'w') as page_file:
        page_file.write(content)
    return file_path
