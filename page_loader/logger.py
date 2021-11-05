import logging

logger = logging.getLogger('page_loader')
handler = logging.StreamHandler()
DEF_LOG_LEVEL = 0  # ERROR


def set_logging_level(level):
    levels = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }
    actual_level = levels.get(level, logging.ERROR)
    logging.basicConfig(level=actual_level)
