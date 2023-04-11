import logging
from sys import stdout


def __setLogger(name: str, stream: bool = False) -> logging.Logger:
    """
    Creates and returns program logger object.

    ---

    :param name: The name of the logger
    :type name: :class:`str`
    :param stream: toggle streaming log to stdout, defaults to `False`.
    :type stream: :class:`bool`
    :return: A logger object
    :rtype: :class:`Logger`
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logFormatter = logging.Formatter(
        '\n[%(asctime)s - %(levelname)s] : %(message)s\n', "%Y-%m-%d %H:%M:%S")

    logHandler = logging.FileHandler(r'.\logs\v2mp3Log.log')
    logHandler.setFormatter(logFormatter)

    streaming = logging.StreamHandler(stdout)

    logger.addHandler(logHandler)

    if stream:
        logger.addHandler(streaming)

    return logger
