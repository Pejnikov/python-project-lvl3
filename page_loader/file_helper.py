from os.path import isdir, join, exists, splitext
from os import makedirs
from re import sub


class ResourceSaver:

    def __init__(self, path, url):
        self.fs_path = path
        self.page_filename = get_name_from_url(url) + '.html'
        self.resource_dir_name = get_name_from_url(url) + '_files'
        self.resource_path = self.make_dir(self.resource_dir_name, self.fs_path)

    def save_page_text(self, content: str) -> str:
        if not isdir(self.fs_path):
            raise ValueError("Directory doesn't exist")
        file_path = join(self.fs_path, self.page_filename)
        with open(file_path, 'w') as page_file:
            page_file.write(content)
        return file_path

    def save_resource(self, content: bytes, url: str) -> str:
        if not isdir(self.fs_path):
            raise ValueError("Directory doesn't exist")
        save_path, extension = splitext(url)
        filename = get_name_from_url(save_path)
        full_name = filename + extension
        save_path = join(self.fs_path, self.resource_dir_name, full_name)
        with open(save_path, 'wb') as resource_file:
            resource_file.write(content)
        return join(self.resource_dir_name, full_name)

    def make_dir(self, name: str, path: str):
        full_path = join(path, name)
        if not exists(full_path):
            makedirs(full_path)
            return full_path


def get_name_from_url(url: str) -> str:
    name_items = []
    url_without_schema = sub(r'^https?:\/\/', '', url)
    for symbol in url_without_schema:
        if symbol.isalpha() or symbol.isdigit():
            name_items.append(symbol)
        else:
            name_items.append('-')
    return ''.join(name_items)
