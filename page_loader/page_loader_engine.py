
from page_loader.file_helper import ResourceSaver
from page_loader.page_content_helper import localize_page
from page_loader.page_content_helper import get_name_from_url
from page_loader.logger import set_logging_level, DEF_LOG_LEVEL


def download(url: str, download_path: str, log_lvl: int = DEF_LOG_LEVEL) -> str:
    set_logging_level(log_lvl)
    saver = ResourceSaver(download_path, get_name_from_url(url) + '_files')
    downloaded_page_path = localize_page(url, saver)
    saver.del_resorce_dir_if_empty()
    return downloaded_page_path
