#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:shana
@file:service.py
@time:2021/11/15
"""
import socket
import sys

from oslo_config import cfg
import oslo_i18n
from oslo_log import log

from pecan_demo.common import defaults
from pecan_demo import messaging
from pecan_demo import version

service_opts = [
    cfg.StrOpt('host',
               default=socket.getfqdn(),
               sample_default='<server-hostname.example.com>',
               help='Name of this node. This can be an opaque identifier. '
                    'It is not necessarily a hostname, FQDN, or IP address. '
                    'However, the node name must be valid within an AMQP key.')
]

cfg.CONF.register_opts(service_opts)


def prepare_service(argv=None, config_files=None):
    if argv is None:
        argv = sys.argv
    #
    # if conf is None:
    #     conf = cfg.ConfigOpts()

    oslo_i18n.enable_lazy()
    log.register_options(cfg.CONF)
    log.set_defaults()
    defaults.set_cors_middleware_defaults()

    cfg.CONF(argv[1:], project='pecan_gai', validate_default_values=True,
         version=version.version_info.version_string(),
         default_config_files=config_files)

    log.setup(cfg.CONF, 'pecan_gai')
    messaging.setup()
    return cfg.CONF