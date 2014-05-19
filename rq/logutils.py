# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

# Make sure that dictConfig is available
# This was added in Python 2.7/3.2
try:
    from logging.config import dictConfig
except ImportError:
    from rq.compat.dictconfig import dictConfig  # noqa


def setup_loghandlers(level=None):
    if not logging._handlers:
        dictConfig({
            'version': 1,
            'disable_existing_loggers': False,

            'formatters': {
                'console': {
                    'format': '%(asctime)s %(message)s',
                    'datefmt': '%H:%M:%S',
                },
            },

            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    # 'class': 'logging.StreamHandler',
                    'class': 'rq.utils.ColorizingStreamHandler',
                    'formatter': 'console',
                    'exclude': ['%(asctime)s'],
                },
            },

            'loggers': {
                'handlers': ['console'],
                'level': level or 'INFO',
            }
        })
