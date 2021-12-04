import os
from page_loader.internal_exceptions import ResourceSavingError  # type: ignore
import logging
import requests

logger = logging.getLogger(__name__)


def handle_fs_exceptions(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PermissionError as err:
            raise ResourceSavingError(
                "Not enough permissions. "
                "The file can't be created."
            ) from err
        except OSError as err:
            raise ResourceSavingError(
                "The file can't be created due to OS-related error."
            ) from err
    return inner


class ResourceSaver:

    def __init__(self, path, resource_dir_name):
        if not os.path.isdir(path):
            raise ResourceSavingError(
                "Directory doesn't exist: '{}'".format(path)
            )
        self.fs_path = path
        self.resource_dir_name = resource_dir_name
        self.resource_dir_path = None

    @handle_fs_exceptions
    def save_page_text(self, content: str, name: str) -> str:
        page_path = os.path.join(self.fs_path, name)
        with open(page_path, 'w') as file:
            file.write(content)
        return page_path

    def save_resource(self, response: requests.Response, filename: str) -> str:
        """
        Checks the presence of resource directory path (it's important to
        create resource directory only if the downloaded page have some
        resources for downloading) then saves data to the resource directory.
        """
        if not self.resource_dir_path:
            self.resource_dir_path = self.make_resource_dir()
        resource_path = os.path.join(
            self.resource_dir_path, filename
        )
        self.save_resource_data(resource_path, response)
        return os.path.join(self.resource_dir_name, filename)

    @handle_fs_exceptions
    def save_resource_data(self, path: str, response: requests.Response):
        """
        Saves the data of resource in stream using chunks in order
        to reduce RAM consuming.
        """
        down_chunk_size = 1024
        with response:
            with open(path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=down_chunk_size):
                    file.write(chunk)

    def make_resource_dir(self):
        full_path = os.path.join(self.fs_path, self.resource_dir_name)
        try:
            os.makedirs(full_path)
        except PermissionError as err:
            raise ResourceSavingError(
                "Not enough permissions. "
                "The directory for page resources can't be created."
            ) from err
        except FileExistsError:
            logger.error("Resources directory already exist:'{}'. It will "
                         "be used for saving page resources".format(full_path))
        except OSError as err:
            raise ResourceSavingError(
                "The directory can't be created due to OS-related error."
            ) from err
        else:
            logger.info(
                'Resources directory was created: {}'.format(full_path)
            )
        return full_path
