
from page_loader.file_helper import ResourceSaver
from page_loader.page_content_helper import localize_page
from page_loader.page_content_helper import get_name_from_url


def download(url: str, download_path: str) -> str:
    saver = ResourceSaver(download_path, get_name_from_url(url) + '_files')
    downloaded_page_path = localize_page(url, saver)
    saver.del_resource_dir_if_empty()
    return downloaded_page_path
