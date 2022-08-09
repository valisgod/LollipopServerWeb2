# -*- coding:utf-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# fh = logging.FileHandler(config.log_dir)
fh = TimedRotatingFileHandler('./log/info.log',
                              when='midnight',
                              interval=1,
                              backupCount=60)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)
