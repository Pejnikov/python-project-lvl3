from typing import Callable
from bs4 import BeautifulSoup  # type: ignore
from progress.bar import FillingCirclesBar   # type: ignore
from urllib.parse import urlparse, urljoin, urlunparse
from os.path import splitext
from page_loader.requests_helper import get_content, get_page_text
from page_loader.file_helper import ResourceSaver
import logging
import hashlib

logger = logging.getLogger(__name__)

IMG_ATTR = 'img'
LINK_ATTR = 'link'
SCRIPT_ATTR = 'script'
REFERENCE_ATTRIBUTE = {
    IMG_ATTR: 'src',
    LINK_ATTR: 'href',
    SCRIPT_ATTR: 'src'
}
SUITABLE_ATR_CONTENT = {
    IMG_ATTR: {'.png', '.jpg'}
}


def localize_page(url: str, saver: ResourceSaver) -> str:
    page_text = get_page_text(url)
    soup = BeautifulSoup(page_text, 'html.parser')
    soup = localize_resources(soup, url, saver)
    page_name = get_resource_name(url)
    return saver.save_page_text(soup.prettify(), page_name)


def localize_resources(
    soup: BeautifulSoup, url: str, saver: ResourceSaver
) -> BeautifulSoup:
    resource_filter = get_resource_filter(url)
    suitable_tags = soup.find_all(resource_filter)
    bar = FillingCirclesBar('Downloading progress:', max=len(suitable_tags))
    for tag in suitable_tags:
        resource_link = tag.get(REFERENCE_ATTRIBUTE[tag.name])
        logger.debug('Trying to download resource: "{}"'.format(resource_link))
        down_link = make_download_link(resource_link, url)
        logger.debug('Link to resource: "{}"'.format(down_link))
        resource_content = get_content(down_link)
        resource_name = get_resource_name(down_link)
        src_path = saver.save_resource(resource_content, resource_name)
        logger.debug('Path to down resource: "{}"'.format(src_path))
        tag[REFERENCE_ATTRIBUTE[tag.name]] = src_path
        bar.next()
    bar.finish()
    return soup


def has_same_domain(src: str, main_url: str) -> bool:
    parsed_url = urlparse(main_url)
    parsed_src = urlparse(src)
    if parsed_src.netloc == '' or parsed_src.netloc == parsed_url.netloc:
        return True
    return False


def has_suitable_content(src: str, tag_name: str) -> bool:
    if tag_name in SUITABLE_ATR_CONTENT.keys():
        extension = splitext(src)[1]
        return extension in SUITABLE_ATR_CONTENT[tag_name]
    return True


def get_resource_filter(url: str) -> Callable[[str], bool]:
    def inner(tag):
        if tag.name in REFERENCE_ATTRIBUTE.keys():
            src = tag.get(REFERENCE_ATTRIBUTE[tag.name])
            logger.debug(
                'Processing the page tag: "{}"'
                ' with resource: "{}"'.format(tag.name, src)
            )
            if src:
                if has_same_domain(src, url):
                    if has_suitable_content(src, tag.name):
                        logger.debug(
                            'The resource is suitable: "{}"'
                            ' with resource: "{}"'.format(tag.name, src)
                        )
                        return True
        return False
    return inner


def make_download_link(url: str, main_url: str) -> str:
    parsed_src = urlparse(url)
    if parsed_src.netloc == '':
        return urljoin(main_url, url)
    return url


def get_resource_name(url: str) -> str:
    parsed_url = urlparse(url)
    path, extension = splitext(parsed_url.path)
    if extension == '':
        extension = '.html'
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
        logger.debug(
            'Hash is used instead of plain name: "{}"'.format(hash_name)
        )
        return hash_name
    else:
        for symbol in url_for_naming:
            if symbol.isalpha() or symbol.isdigit():
                name_items.append(symbol)
            else:
                name_items.append('-')
        return ''.join(name_items)
