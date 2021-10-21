
from page_loader.file_helper import save_page_text, get_name_from_url
from page_loader.file_helper import make_directory
from page_loader.requests_helper import get_page_text
from page_loader.page_content_helper import localize_page_pictures


def download(url: str, download_path: str) -> str:
    root_directory_name = get_name_from_url(url)
    resources_directory_name = root_directory_name + '_files'
    resources_path = make_directory(resources_directory_name, download_path)
    page_name = root_directory_name + '.html'
    page_text = get_page_text(url)
    localize_page_pictures(page_text, url, resources_path)
    downloaded_file_path = save_page_text(download_path, page_name, page_text)
    return downloaded_file_path
