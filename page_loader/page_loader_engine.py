
from page_loader.file_helper import ResourceSaver
from page_loader.requests_helper import get_page_text
from page_loader.page_content_helper import localize_page_pictures


def download(url: str, download_path: str) -> str:
    saver = ResourceSaver(download_path, url)
    page_text = get_page_text(url)
    downloaded_file_path = localize_page_pictures(page_text, url, saver)
    return downloaded_file_path
