from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from page_loader.requests_helper import get_page_content
from os.path import splitext


def has_same_domen(src: str, main_url: str) -> bool:
    parsed_url = urlparse(main_url)
    parsed_src = urlparse(src)
    if parsed_src.netloc == '' or parsed_src.netloc.endswith(parsed_url.netloc):
        return True
    return False


def refers_to_suitable_content(src: str) -> bool:
    supported_formats = {'.png', '.jpg'}
    extension = splitext(src)[1]
    if extension in supported_formats:
        return True
    return False


def make_download_link(url: str, main_url: str) -> str:
    parsed_src = urlparse(url)
    if parsed_src.netloc == '':
        return urljoin(main_url, url)
    return url


def localize_page_pictures(page: str, url: str, path: str):
    soup = BeautifulSoup(page, 'html.parser')
    image_tags = soup.find_all('img')
    image_srcs = []
    for tag in image_tags:
        image_srcs.append(tag.get('src'))
    srcs_to_localize = []
    for src in image_srcs:
        if has_same_domen(src, url) and refers_to_suitable_content(src):
            srcs_to_localize.append(src)
    for src in srcs_to_localize:
        down_link = make_download_link(src, url)
        src_content = get_page_content(down_link)
        


