from page_loader.page_loader_engine import download
from os.path import abspath, basename, isfile
import requests_mock
import tempfile



def test_page_download():
    test_url = 'https://semver.org/lang/ru'
    test_page_path = 'tests/fixtures/web_page.html'
    expected_file_name = 'semver-org-lang-ru.html'
    with open(abspath(test_page_path), 'r') as file:
        test_page_text = file.read()
        with requests_mock.Mocker() as m:
            m.get(test_url, text=test_page_text)
            with tempfile.TemporaryDirectory() as tmpdirname:
                downloaded_file_path = download(test_url, tmpdirname)
                assert expected_file_name == basename(downloaded_file_path)
                assert isfile(downloaded_file_path)
                with open(abspath(downloaded_file_path), 'r') as page_file:
                    downloaded_text = page_file.read()
                assert test_page_text == downloaded_text

        