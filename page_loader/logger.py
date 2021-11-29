import logging

DEF_LOG_LEVEL = 0  # ERROR


logger = logging.getLogger('page_loader')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def set_logging_level(log_lvl: int = DEF_LOG_LEVEL):
    levels = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }
    actual_level = levels.get(log_lvl, logging.ERROR)
    logger.setLevel(actual_level)
