from page_loader.page_loader_engine import download
from page_loader.internal_exceptions import ResourceSavingError
from page_loader.internal_exceptions import PageRequestError
from page_loader.file_helper import handle_fs_exceptions
import logging
import pytest
import os

test_page_url = 'https://ru.hexlet.io/courses'


def test_resource_dir_permissions(requests_mock, tmp_path):
    requests_mock.get(test_page_url, text='TEST')
    os.chmod(tmp_path, 0o444)
    with pytest.raises(ResourceSavingError):
        download(test_page_url, tmp_path)


def test_resource_dir_exist(requests_mock, tmp_path, caplog):
    exp_dir_name = 'ru-hexlet-io-courses_files'
    test_resource_link = 'https://ru.hexlet.io/test.css'
    os.makedirs(os.path.join(tmp_path, exp_dir_name))
    requests_mock.get(
        test_page_url,
        text='<link href="{}"/>'.format(test_resource_link)
    )
    requests_mock.get(test_resource_link, text='test')
    with caplog.at_level(logging.ERROR):
        download(test_page_url, tmp_path)
    assert 'Resources directory already exist' in caplog.text


def test_OS_errors_handling():
    def get_test_exception():
        raise TimeoutError
    with pytest.raises(ResourceSavingError):
        handle_fs_exceptions(get_test_exception)()


def test_invalid_url(requests_mock, tmp_path):
    test_page_url = '//ru.hexlet.io/courses'
    requests_mock.get(test_page_url, text='TEST')
    with pytest.raises(PageRequestError):
        download(test_page_url, tmp_path)


def test_403_exception(requests_mock, tmp_path):
    requests_mock.get(test_page_url, text='TEST', status_code=403)
    with pytest.raises(PageRequestError):
        download(test_page_url, tmp_path)
