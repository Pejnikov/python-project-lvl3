from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urlparse, urljoin
from os.path import splitext
from page_loader.requests_helper import get_page_content, get_page_text
from page_loader.file_helper import PageSaver
import logging

logger = logging.getLogger('page_loader.content_helper')

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
    saver: PageSaver
):
    page_tags = soup.find_all(resource_tag)
    for tag in page_tags:
        src = tag.get(TAGS_SOURCES[resource_tag])
        if src:
            logger.debug('Trying to download resource: "{}"'.format(src))
            if is_same_domen(src, url) and has_suitable_content(src, tag.name):
                down_link = make_download_link(src, url)
                logger.debug('Link to resource: "{}"'.format(down_link))
                src_content = get_page_content(down_link)
                src_path = saver.save_resource(src_content, down_link)
                logger.debug('Path to down resource: "{}"'.format(src_path))
                tag[TAGS_SOURCES[resource_tag]] = src_path
    return soup


def localize_page_resources(url: str, saver: PageSaver) -> str:
    page_text = get_page_text(url)
    soup = BeautifulSoup(page_text, 'html.parser')
    for tag in TAGS_SOURCES.keys():
        logger.debug('Processing the page tag: "{}"'.format(tag))
        soup = localize_resource(soup, tag, url, saver)
    return saver.save_page_text(soup.prettify(), url)
