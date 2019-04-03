import logging

fmt = "%(asctime)s %(name)s %(levelname)s: %(message)s"

def init_logger(level=logging.INFO, log_file=None):
    logging.root.handlers = []
    logger = logging.getLogger('')
    logger.setLevel(level)

    sh = logging.StreamHandler()
    sh.setLevel(level)
    sh.setFormatter(logging.Formatter(fmt))
    logger.addHandler(sh)

    if log_file is not None:
        fh = logging.FileHandler(log_file)
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter(fmt))
        logger.addHandler(fh)



