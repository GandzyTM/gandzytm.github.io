import logging

formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
handler = logging.FileHandler(filename="logging.log")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
