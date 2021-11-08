from os.path import isdir, join, exists, splitext
from os import makedirs
from re import sub
from typing import Union
from page_loader.internal_exceptions import ResourceSavingError  # type: ignore
import logging


logger = logging.getLogger('page_loader.file_helper')


class PageSaver:

    def __init__(self, path, url):
        if not isdir(path):
            raise ResourceSavingError("Directory "
                                      "doesn't exist: '{}'".format(path))
        self.fs_path = path
        self.resource_dir_name = get_name_from_url(url) + '_files'
        self.resource_path = self.make_resource_dir()

    def save_page_text(self, content: str, url: str) -> str:
        file_extension = '.html'
        page_filename = get_name_from_url(url) + file_extension
        page_path = join(self.fs_path, page_filename)
        self.save_resource_data(page_path, content)
        return page_path

    def save_resource(self, content: bytes, url: str) -> str:
        main_url, extension = splitext(url)
        filename = get_name_from_url(main_url)
        full_name = filename + extension
        resource_path = join(self.fs_path, self.resource_dir_name, full_name)
        self.save_resource_data(resource_path, content)
        return join(self.resource_dir_name, full_name)

    def save_resource_data(self, path: str, data: Union[bytes, str]):
        data_type = type(data)
        write_mode = {bytes: 'wb', str: 'w'}.get(data_type, 'wb')
        with open(path, write_mode) as file:
            file.write(data)

    def make_resource_dir(self):
        full_path = join(self.fs_path, self.resource_dir_name)
        if not exists(full_path):
            try:
                makedirs(full_path)
            except PermissionError as err:
                raise ResourceSavingError("Not enough permissions. "
                                          "The directory for page resources "
                                          "can't be created.") from err
            else:
                logger.info('Resources directory '
                            'was created: {}'.format(full_path))
        else:
            logger.warning('The page resource directory already exists')
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
