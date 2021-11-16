import os
from typing import Union
from page_loader.internal_exceptions import ResourceSavingError  # type: ignore
import logging


logger = logging.getLogger('page_loader.file_helper')


class ResourceSaver:

    def __init__(self, path, resource_dir_name):
        if not os.path.isdir(path):
            raise ResourceSavingError(
                "Directory doesn't exist: '{}'".format(path)
            )
        self.fs_path = path
        self.resource_dir_name = resource_dir_name
        self.resource_path = self.make_resource_dir()

    def save_page_text(self, content: str, name: str) -> str:
        page_path = os.path.join(self.fs_path, name)
        self.save_resource_data(page_path, content)
        return page_path

    def save_resource(self, content: bytes, resource_name: str) -> str:
        resource_path = os.path.join(
            self.fs_path,
            self.resource_dir_name,
            resource_name
        )
        self.save_resource_data(resource_path, content)
        return os.path.join(self.resource_dir_name, resource_name)

    def save_resource_data(self, path: str, data: Union[bytes, str]):
        data_type = type(data)
        write_mode = {bytes: 'wb', str: 'w'}.get(data_type, 'wb')
        try:
            with open(path, write_mode) as file:
                file.write(data)
        except PermissionError as err:
            raise ResourceSavingError(
                "Not enough permissions. "
                "The file can't be created: {}".format(path)
            ) from err
        else:
            logger.info(
                'Resource was saved: {}'.format(path)
            )

    def make_resource_dir(self):
        full_path = os.path.join(self.fs_path, self.resource_dir_name)
        try:
            os.makedirs(full_path)
        except PermissionError as err:
            raise ResourceSavingError(
                "Not enough permissions. "
                "The directory for page resources can't be created."
            ) from err
        except FileExistsError as err:
            raise ResourceSavingError(
                "The page resource directory already exists"
            ) from err
        else:
            logger.info(
                'Resources directory was created: {}'.format(full_path)
            )
        return full_path

    def del_resorce_dir_if_empty(self):
        if not os.listdir(self.resource_path):
            os.rmdir(self.resource_path)
