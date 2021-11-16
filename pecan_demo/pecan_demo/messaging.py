#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 11:05
# @Author   :shana
# @File     :messaging.py
from oslo_config import cfg
import oslo_messaging
# from oslo_messaging.rpc import dispatcher
from oslo_messaging.notify import notifier
from oslo_messaging import serializer as oslo_serializer

DEFAULT_URL = "__default__"
RPC_TARGET = None
TRANSPORTS = {}


def setup():
    oslo_messaging.set_transport_defaults('pecan_demo')


def get_transport(conf=None, url=None, optional=False, cache=True):
    """Initialise the oslo_messaging layer."""
    global TRANSPORTS, DEFAULT_URL
    cache_key = url or DEFAULT_URL
    transport = TRANSPORTS.get(cache_key)
    if not transport or not cache:
        try:
            transport = notifier.get_notification_transport(cfg.CONF, url)
        except (oslo_messaging.InvalidTransportURL,
                oslo_messaging.DriverLoadFailure):
            if not optional or url:
                # NOTE(sileht): oslo_messaging is configured but unloadable
                # so reraise the exception
                raise
            return None
        else:
            if cache:
                TRANSPORTS[cache_key] = transport
    return transport


def get_target():
    global RPC_TARGET
    if RPC_TARGET is None:
        RPC_TARGET = oslo_messaging.Target(topic='pecan_demo', version='0.1')
    return RPC_TARGET


# def get_client(version_cap=None):
#     transport = get_transport()
#     target = get_target()
#     return oslo_messaging.RPCClient(transport, target, version_cap=version_cap)


# def get_server(target=None, endpoints=None):
#     access_policy = dispatcher.DefaultRPCAccessPolicy
#     transport = get_transport()
#     if not target:
#         target = get_target()
#     return oslo_messaging.get_rpc_server(transport, target,
#                                          endpoints, executor='eventlet',
#                                          access_policy=access_policy)


def cleanup():
    """Cleanup the oslo_messaging layer."""
    global TRANSPORTS, NOTIFIERS
    NOTIFIERS = {}
    for url in TRANSPORTS:
        TRANSPORTS[url].cleanup()
        del TRANSPORTS[url]


_SERIALIZER = oslo_serializer.JsonPayloadSerializer()


def get_batch_notification_listener(transport, targets, endpoints,
                                    allow_requeue=False,
                                    batch_size=1, batch_timeout=None):
    """Return a configured oslo_messaging notification listener."""
    return oslo_messaging.get_batch_notification_listener(
        transport, targets, endpoints, executor='threading',
        allow_requeue=allow_requeue,
        batch_size=batch_size, batch_timeout=batch_timeout)


def get_notifier(transport=None, publisher_id=''):
    """Return a configured oslo_messaging notifier."""
    if not transport:
        transport = get_transport()
    notifier = oslo_messaging.Notifier(transport, serializer=_SERIALIZER)
    return notifier.prepare(publisher_id=publisher_id)


def get_msg_info():
    msg_info = dict(
        description='',
        state='',
        project_id=''
    )
    return msg_info
