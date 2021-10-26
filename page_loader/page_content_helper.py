from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urlparse, urljoin
from typing import Dict, List, Any

from page_loader.requests_helper import get_page_content
from page_loader.file_helper import ResourceSaver
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


def localize_page_pictures(page: str, url: str, saver: ResourceSaver) -> str:
    soup = BeautifulSoup(page, 'html.parser')
    image_tags = soup.find_all('img')
    srcs_to_localize = get_srcs_to_localize(image_tags, url)
    localized_srcs = get_localized_srcs(srcs_to_localize, url, saver)
    for tag in image_tags:
        tag_src = tag.get('src')
        if tag_src in localized_srcs:
            tag['src'] = localized_srcs[tag_src]
    return saver.save_page_text(soup.prettify())


def get_srcs_to_localize(image_tags: Any, url: str) -> Any:
    image_srcs = []
    srcs_to_localize = []
    for tag in image_tags:
        image_srcs.append(tag.get('src'))
    for src in image_srcs:
        if has_same_domen(src, url) and refers_to_suitable_content(src):
            srcs_to_localize.append(src)
    return srcs_to_localize


def get_localized_srcs(
    srcs_to_localize: List[str],
    url: str,
    saver: ResourceSaver
) -> Dict[str, str]:
    localized_srcs = {}
    for src in srcs_to_localize:
        down_link = make_download_link(src, url)
        src_content = get_page_content(down_link)
        src_path = saver.save_resource(src_content, down_link)
        localized_srcs[src] = src_path
    return localized_srcs
