# coding=utf-8

import logging.config

from conf.log_conf import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
logger.info("..让我..入梦...")
