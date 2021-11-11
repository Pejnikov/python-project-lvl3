from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urlparse, urljoin, urlunparse
from os.path import splitext
from page_loader.requests_helper import get_page_content, get_page_text
from page_loader.file_helper import ResourceSaver
import logging
import hashlib

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
    saver: ResourceSaver
) -> BeautifulSoup:
    page_tags = soup.find_all(resource_tag)
    for tag in page_tags:
        src = tag.get(TAGS_SOURCES[resource_tag])
        if src:
            logger.debug('Trying to download resource: "{}"'.format(src))
            if is_same_domen(src, url) and has_suitable_content(src, tag.name):
                down_link = make_download_link(src, url)
                logger.debug('Link to resource: "{}"'.format(down_link))
                src_content = get_page_content(down_link)
                resource_name = get_resource_name(down_link)
                src_path = saver.save_resource(src_content, resource_name)
                logger.debug('Path to down resource: "{}"'.format(src_path))
                tag[TAGS_SOURCES[resource_tag]] = src_path
    return soup


def localize_page_resources(url: str, saver: ResourceSaver) -> str:
    page_text = get_page_text(url)
    soup = BeautifulSoup(page_text, 'html.parser')
    for tag in TAGS_SOURCES.keys():
        logger.debug('Processing the page tag: "{}"'.format(tag))
        soup = localize_resource(soup, tag, url, saver)
    page_name = get_page_name(url)
    return saver.save_page_text(soup.prettify(), page_name)


def get_page_name(url:str) -> str:
    file_extension = '.html'
    return get_name_from_url(url) + file_extension


def get_resource_name(url: str) -> str:
    parsed_url = urlparse(url)
    path, extension = splitext(parsed_url.path)
    parsed_url = parsed_url._replace(path=path)
    filename = get_name_from_url(urlunparse(parsed_url))
    resource_name = filename + extension
    return resource_name


def get_name_from_url(url: str) -> str:
    name_items = []
    parsed_url = urlparse(url)._replace(scheme='')
    url_for_naming = urlunparse(parsed_url).strip('//')
    if parsed_url.query != '':
        hash_name = hashlib.md5(url_for_naming.encode('utf-8')).hexdigest()
        logger.debug('Hash is used instead of plain name: "{}"'.format(hash_name))
        return hash_name
    else:
        for symbol in url_for_naming:
            if symbol.isalpha() or symbol.isdigit():
                name_items.append(symbol)
            else:
                name_items.append('-')
        return ''.join(name_items)
