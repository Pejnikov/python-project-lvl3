from page_loader.page_loader_engine import download
from page_loader.internal_exceptions import ResourceSavingError
from page_loader.internal_exceptions import PageRequestError
import pytest
import os


def test_resource_dir_permissions(requests_mock, tmp_path):
    test_page_url = 'https://ru.hexlet.io/courses'
    requests_mock.get(test_page_url, text='TEST')
    os.chmod(tmp_path, 0o444)
    with pytest.raises(ResourceSavingError):
        download(test_page_url, tmp_path)


def test_resource_dir_exist(requests_mock,tmp_path):
        test_page_url = 'https://ru.hexlet.io/courses'
        exp_dir_name = 'ru-hexlet-io-courses_files'
        os.makedirs(os.path.join(tmp_path, exp_dir_name))
        requests_mock.get(test_page_url, text='TEST')
        with pytest.raises(ResourceSavingError):
            download(test_page_url, tmp_path)


def test_resource_exist(requests_mock,tmp_path):
        test_page_url = 'https://ru.hexlet.io/courses'
        requests_mock.get(test_page_url, text='TEST')
        download(test_page_url, tmp_path)
        with pytest.raises(ResourceSavingError):
            download(test_page_url, tmp_path)


def test_invalid_url(requests_mock,tmp_path):
        test_page_url = '//ru.hexlet.io/courses'
        requests_mock.get(test_page_url, text='TEST')
        with pytest.raises(PageRequestError):
            download(test_page_url, tmp_path)


def test_403_exception(requests_mock,tmp_path):
        test_page_url = 'https://ru.hexlet.io/courses'
        requests_mock.get(test_page_url, text='TEST', status_code=403)
        with pytest.raises(PageRequestError):
            download(test_page_url, tmp_path)