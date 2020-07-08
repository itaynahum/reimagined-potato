import logging


class Config:
    """
    Configurations.
    CONSTANTS
    CONFIGURABLE
    VARIABLES
    """
    RUN = True

    LOG_FORMAT = '%(asctime)s|%(name)s|%(levelname)s - %(message)s'
    LOG_LEVEL = logging.DEBUG

    PORT = 5678
    HOST = '192.168.1.167'

    ACCEPT_CONNECTION_LIMIT = 5

    BUFFER = 5000

    QUIT_MESSAGE = '!QUIT'

    STRING_FORMAT = 'utf-8'


def init_logger():
    """
    Creating Logger
    :return: C(Logger)
    """
    logger = logging.getLogger('__main__')
    logger.setLevel(Config.LOG_LEVEL)

    ch = logging.StreamHandler()
    ch.setLevel(Config.LOG_LEVEL)

    formatter = logging.Formatter(Config.LOG_FORMAT)

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger
