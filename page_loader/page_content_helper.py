from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urlparse, urljoin
from page_loader.requests_helper import get_page_content
from page_loader.file_helper import ResourceSaver
from os.path import splitext


TAGS_SOURCES = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def is_same_domen(src: str, main_url: str) -> bool:
    parsed_url = urlparse(main_url)
    parsed_src = urlparse(src)
    if parsed_src.netloc == '' or parsed_src.netloc.endswith(parsed_url.netloc):
        return True
    return False


def has_suitable_content(src: str, tag_name: str) -> bool:
    supported_formats = {'.png', '.jpg'}
    if tag_name == 'img':
        extension = splitext(src)[1]
        return extension in supported_formats
    return True


def make_download_link(url: str, main_url: str) -> str:
    parsed_src = urlparse(url)
    if parsed_src.netloc == '':
        return urljoin(main_url, url)
    return url


def localize_resource(
    soup: BeautifulSoup,
    resource_tag: str,
    url: str,
    saver: ResourceSaver
):
    page_tags = soup.find_all(resource_tag)
    for tag in page_tags:
        src = tag.get(TAGS_SOURCES[resource_tag])
        if is_same_domen(src, url) and has_suitable_content(src, tag.name):
            down_link = make_download_link(src, url)
            src_content = get_page_content(down_link)
            src_path = saver.save_resource(src_content, down_link)
            tag[TAGS_SOURCES[resource_tag]] = src_path
    return soup


def localize_page_resources(page: str, url: str, saver: ResourceSaver) -> str:
    soup = BeautifulSoup(page, 'html.parser')
    for tag in TAGS_SOURCES.keys():
        soup = localize_resource(soup, tag, url, saver)
    return saver.save_page_text(soup.prettify())
