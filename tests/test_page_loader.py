from page_loader.page_loader_engine import download
from page_loader.page_content_helper import get_name_from_url
from os.path import abspath, isfile, split, join
import os
import pytest


def test_images_download(requests_mock, tmp_path):
    test_page_url = 'https://ru.hexlet.io/courses'
    test_page_path = 'tests/fixtures/images_download/initial_web_page.html'
    test_img_url = 'https://ru.hexlet.io/assets/professions/nodejs.png'
    test_img_path = 'tests/fixtures/images_download/Image.png'
    test_img1_url = 'https://ru.hexlet.io/image1.jpg'
    test_img1_path = 'tests/fixtures/images_download/Image1.jpg'
    exp_page_file_name = 'ru-hexlet-io-courses.html'
    exp_page_path = 'tests/fixtures/images_download/exp_web_page.html'
    exp_img_names = ['ru-hexlet-io-assets-professions-nodejs.png', 'ru-hexlet-io-image1.jpg']
    exp_dir_name = 'ru-hexlet-io-courses_files'
    # Mock test page and its resources
    with open(abspath(test_page_path), 'r') as file, \
         open(abspath(test_img_path), 'br') as image, \
         open(abspath(test_img1_path), 'br') as image1:
        test_page_text = file.read()
        test_img_content = image.read()
        test_img1_content = image1.read()
        requests_mock.get(test_page_url, text=test_page_text)
        requests_mock.get(test_img_url, content=test_img_content)
        requests_mock.get(test_img1_url, content=test_img1_content)
        # Test that page text is downloaded and saved
        down_page_path = download(test_page_url, tmp_path)
        assert isfile(down_page_path)
        path, down_page_file_name = split(down_page_path)
        assert exp_page_file_name == down_page_file_name
        with open(abspath(down_page_path), 'r') as page_file, \
             open(abspath(exp_page_path), 'r') as exp_page_file:
            down_page_text = page_file.read()
            exp_page_text = exp_page_file.read()
        assert exp_page_text == down_page_text
        # Test that only directory with images is created
        _, dirs, _ = next(os.walk(path))
        assert [exp_dir_name] == dirs
        # Test that only particular images are downloaded
        page_resources_path = join(path, exp_dir_name)
        _, _, filenames = next(os.walk(page_resources_path))
        assert exp_img_names == filenames
        # Test that downloaded resource have the expected content
        downloaded_image_path = join(page_resources_path, exp_img_names[0])
        with open(abspath(downloaded_image_path), 'br') as downloaded_file:
            downloaded_file_content = downloaded_file.read()
        assert test_img_content == downloaded_file_content


def test_links_scripts_download(requests_mock, tmp_path):
    test_page_url = 'https://ru.hexlet.io/courses'
    test_page_path = 'tests/fixtures/links_scripts_download/initial_web_page.html'
    test_css_url = 'https://ru.hexlet.io/assets/application.css'
    test_css_path = 'tests/fixtures/links_scripts_download/Sheet.css'
    test_script_url = 'https://ru.hexlet.io/packs/js/runtime.js'
    test_script_path = 'tests/fixtures/links_scripts_download/Script.js'
    exp_page_file_name = 'ru-hexlet-io-courses.html'
    exp_page_path = 'tests/fixtures/links_scripts_download/exp_web_page.html'
    exp_resources_names = ['ru-hexlet-io-packs-js-runtime.js', 'ru-hexlet-io-assets-application.css']
    exp_dir_name = 'ru-hexlet-io-courses_files'
    # Mock test page and its resources
    with open(abspath(test_page_path), 'r') as file, \
         open(abspath(test_css_path), 'r') as sheet, \
         open(abspath(test_script_path), 'r') as script:
        test_page_text = file.read()
        test_css_content = sheet.read()
        test_script_content = script.read()
        requests_mock.get(test_page_url, text=test_page_text)
        requests_mock.get(test_css_url, text=test_css_content)
        requests_mock.get(test_script_url, text=test_script_content)
        # Test that page text is downloaded and saved
        down_page_path = download(test_page_url, tmp_path)
        assert isfile(down_page_path)
        path, down_page_file_name = split(down_page_path)
        assert exp_page_file_name == down_page_file_name
        with open(abspath(down_page_path), 'r') as page_file, \
             open(abspath(exp_page_path), 'r') as exp_page_file:
            down_page_text = page_file.read()
            exp_page_text = exp_page_file.read()
        assert exp_page_text == down_page_text
        # Test that only directory with images is created
        _, dirs, _ = next(os.walk(path))
        assert [exp_dir_name] == dirs
        # Test that only particular resources are downloaded
        page_resources_path = join(path, exp_dir_name)
        _, _, filenames = next(os.walk(page_resources_path))
        assert exp_resources_names == filenames
        # Test that downloaded resources have the expected content
        downloaded_css_path = join(page_resources_path, exp_resources_names[1])
        downloaded_script_path = join(page_resources_path, exp_resources_names[0])
        with open(abspath(downloaded_css_path), 'r') as css, \
            open(abspath(downloaded_script_path), 'r') as script:
            downloaded_css_content = css.read()
            downloaded_script_content = script.read()
        assert test_css_content == downloaded_css_content
        assert test_script_content == downloaded_script_content


@pytest.mark.parametrize("input_url,expected_name",[(
    "https://ru.hexlet.io/courses", "ru-hexlet-io-courses",
),(
    "https://en.wikipedia.org/w/index?title=Wikipedia:Images&action=edit","b5e1f513e6fd45c3dcc2e029a8ebf274",
)
]
)
def test_content_file_names(input_url, expected_name):
    result_name = get_name_from_url(input_url)
    assert result_name == expected_name
