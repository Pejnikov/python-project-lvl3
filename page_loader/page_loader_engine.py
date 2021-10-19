
from page_loader.file_helper import save_page_text, get_name_from_url
from page_loader.requests_helper import get_page_text
from page_loader.page_content_helper import localize_page_pictures


def download(url: str, download_path: str) -> str:
    page_text = get_page_text(url)
    root_name = get_name_from_url(url)
    page_name = root_name + '.html'
    localize_page_pictures(page_text, url, download_path)
    downloaded_file_path = save_page_text(download_path, page_name, page_text)
    return downloaded_file_path
