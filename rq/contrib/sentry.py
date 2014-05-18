# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

_clients = {}


def get_client(dsn):
    """
    Gets a copy of the Sentry client usable for the current process.  This
    makes sure we can still reliably use Sentry after an os.fork().
    """
    global _clients
    from raven import Client

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
    from raven import Client

    if isinstance(dsn, Client):
        raise TypeError('Starting with RQ 0.4.6, the first argument to register_sentry() should be the DSN string, not a Client instance anymore.')

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
