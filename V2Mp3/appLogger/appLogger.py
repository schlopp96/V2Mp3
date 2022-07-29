import logging


def setLogger(name) -> logging.Logger:
    """
    Creates and returns program logger object.

    ---

    :param name: The name of the logger
    :type name: :class:`str`
    :return: A logger object
    :rtype: :class:`logging.Logger`
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logFormatter = logging.Formatter(
        '[%(asctime)s - %(levelname)s] : %(message)s\n', "%Y-%m-%d %H:%M:%S")

    logHandler = logging.FileHandler(r'.\logs\v2mp3Log.log')
    logHandler.setFormatter(logFormatter)

    logger.addHandler(logHandler)
    return logger
