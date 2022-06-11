import logging


def applogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logFormatter = logging.Formatter(
        '[%(asctime)s - %(levelname)s] : %(message)s\n', "%Y-%m-%d %H:%M:%S")

    logHandler = logging.FileHandler(r'.\logs\v2mp3Log.log', 'a')
    logHandler.setFormatter(logFormatter)

    logger.addHandler(logHandler)
    return logger