from page_loader.page_loader_engine import download
from page_loader.file_helper import get_name_from_url
from page_loader.page_content_helper import need_localize
from os.path import abspath, isfile, isdir, split, join
import pytest


def test_page_text_download(requests_mock, tmp_path):
    test_url = 'https://ru.hexlet.io/courses'
    test_page_path = 'tests/fixtures/web_page.html'
    exp_file_name = 'ru-hexlet-io-courses.html'
    # Test that page text is downloaded
    with open(abspath(test_page_path), 'r') as file:
        test_page_text = file.read()
        requests_mock.get(test_url, text=test_page_text)
        downloaded_file_path = download(test_url, tmp_path)
        print(downloaded_file_path)
        assert isfile(downloaded_file_path)
        path, filename = split(downloaded_file_path)
        assert filename == exp_file_name
        with open(abspath(downloaded_file_path), 'r') as page_file:
            downloaded_text = page_file.read()
        assert test_page_text == downloaded_text
        # Test that images are downloaded

        exp_images_dir_name = 'ru-hexlet-io-courses_files'
        print(join(path, exp_images_dir_name))
        assert isdir(join(path, exp_images_dir_name))


@pytest.mark.parametrize("input_url,expected_name",[(
    "https://ru.hexlet.io/courses", "ru-hexlet-io-courses",
)
]
)
def test_content_file_names(input_url, expected_name):
    assert get_name_from_url(input_url) == expected_name

'''
@pytest.mark.parametrize("url,resolution",[(
    "/test/image1.png", True,
), (
    "http://test.com/test/image2.png", True,
), (
    "http://test.com/test/image3.jpg", True,
), (
    "http://project.test.com/test/image4.png", True,
), (
    "http://project.different_domen.com/test/image5.png", False,
)
]
)
def test_need_localize_resource(url, resolution):
    assert need_localize(url) == resolution


def test_localize_pictures(requests_mock, tmp_path):
    test_page_url = 'http://test.com'
    test_page_path = '/tests/fixtures/images_downloading/web_page_with_imgs.html'
    test_img_url = 'http://test.com/test/image.png'
    test_img_url1 = 'http://test.com/test/image1.png'
    test_img_file = 'tests/fixtures/images_downloading/Image.png'
    test_img_file1 = 'tests/fixtures/images_downloading/Image1.jpg'
    with open(abspath(test_img_file)), 'br' as image, \
         open(abspath(test_img_file1)), 'br' as image1, \
         open(abspath(test_page_path)), 'r' as test_page:
        test_img_content = image.read()
        test_img_content1 = image1.read()
        test_page_text = test_page.read()
        requests_mock.get(test_img_url, content=test_img_content)
        requests_mock.get(test_img_url1, content=test_img_content1)
        localize_page_pictures(test_page_text, test_page_url, tmp_path)
        assert isdir('test-com_files')
'''

