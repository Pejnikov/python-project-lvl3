from page_loader.page_loader_engine import download
from page_loader.file_helper import get_name_from_url
from os.path import abspath, isfile, isdir, split, join
import pytest


def test_page_text_download(requests_mock, tmp_path):
    test_page_url = 'https://ru.hexlet.io/courses'
    test_page_path = 'tests/fixtures/web_page.html'
    test_img_url = 'https://ru.hexlet.io/test/image.png'
    test_img_path = 'tests/fixtures/images_downloading/Image.png'
    test_img1_url = 'https://ru.hexlet.io/image1.jpg'
    test_img1_path = 'tests/fixtures/images_downloading/Image1.jpg'
    exp_page_file_name = 'ru-hexlet-io-courses.html'
    exp_img_name = 'ru-hexlet-io-test-image.png'
    exp_img1_name = 'ru-hexlet-io-image1.jpg'
    exp_resources_dir_name = 'ru-hexlet-io-courses_files'
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
        assert down_page_file_name == exp_page_file_name
        with open(abspath(down_page_path), 'r') as page_file:
            down_page_text = page_file.read()
        assert test_page_text == down_page_text
        # Test that path with images is created
        page_resources_path = join(path, exp_resources_dir_name)
        assert isdir(page_resources_path)
        # Test that images are downloaded
        down_img_path = join(page_resources_path, exp_img_name)
        down_img1_path = join(page_resources_path, exp_img1_name)
        #assert isfile(down_img_path)
        #assert isfile(down_img1_path)




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

