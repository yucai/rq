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


def setup_loghandlers(level=None, sentry_dsn=None):
    if not logging._handlers:
        formatters = {
            'rq_console': {
                'format': '%(asctime)s %(message)s',
                'datefmt': '%H:%M:%S',
            },
        }

        handlers = {
            'rq_console': {
                'level': 'DEBUG',
                # 'class': 'logging.StreamHandler',
                'class': 'rq.utils.ColorizingStreamHandler',
                'formatter': 'rq_console',
                'exclude': ['%(asctime)s'],
            },
        }

        loggers = {
            'rq.worker': {
                'handlers': ['rq_console'],
                'level': level or 'INFO',
            },
        }

        if sentry_dsn:
            handlers['rq_sentry'] = {
                'level': 'ERROR',
                'class': 'raven.handlers.logging.SentryHandler',
                'dsn': sentry_dsn,
            }

            loggers['rq.worker']['handlers'] += ['rq_sentry']

        dictConfig({
            'version': 1,
            'disable_existing_loggers': False,

            'formatters': formatters,
            'handlers': handlers,
            'loggers': loggers,
        })
