# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from raven import Client

_clients = {}


def get_client(dsn):
    """
    Gets a copy of the Sentry client usable for the current process.  This
    makes sure we can still reliably use Sentry after an os.fork().
    """
    global _clients

    pid = os.getpid()
    client = _clients.get(pid)
    if client is None:
        _clients[pid] = client = Client(dsn)

    return client


def register_sentry(dsn, worker):
    """
    Given a Raven client and an RQ worker, registers exception handlers with
    the worker so exceptions are logged to Sentry.
    """
    def send_to_sentry(job, *exc_info):
        client = get_client(dsn)
        client.captureException(
            exc_info=exc_info,
            extra={
                'job_id': job.id,
                'func': job.func_name,
                'args': job.args,
                'kwargs': job.kwargs,
                'description': job.description,
            })

    worker.push_exc_handler(send_to_sentry)
