
from page_loader.file_helper import ResourceSaver
from page_loader.page_content_helper import localize_page_resources
from page_loader.logger import set_logging_level, DEF_LOG_LEVEL


def download(url: str, download_path: str, log_lvl: int = DEF_LOG_LEVEL) -> str:
    set_logging_level(log_lvl)
    saver = ResourceSaver(download_path, url)
    downloaded_page_path = localize_page_resources(url, saver)
    return downloaded_page_path
