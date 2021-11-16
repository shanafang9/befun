#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 10:29
# @Author   :shana
# @File     :app.py
import os

from oslo_config import cfg

from oslo_log import log
from paste import deploy
import pecan

from pecan_demo.api import config as api_config
from pecan_demo.api import hooks
from pecan_demo import service

LOG = log.getLogger(__name__)

default_opts = [
    cfg.StrOpt('test'),
]

auth_opts = [
    cfg.StrOpt('api_paste_config',
               default="api_paste.ini",
               help="Configuration file for WSGI definition of API."),
    cfg.StrOpt('auth_strategy',
               choices=['noauth', 'keystone'],
               default='keystone',
               help=("The strategy to use for auth. Supports noauth and "
                     "keystone")),
]

api_opts = [
    cfg.IPOpt('host_ip',
              default='0.0.0.0',
              help='The listen IP for the pecan_demo API server.'),
    cfg.PortOpt('port',
                default=8889,
                help='The port for the pecan_demo API server.'),
    cfg.BoolOpt('pecan_debug',
                default=False,
                help='Toggle Pecan Debug Middleware.'),
]

CONF = cfg.CONF
CONF.register_opts(default_opts, group='DEFAULT')
CONF.register_opts(auth_opts)
CONF.register_opts(api_opts, group='api')


def get_pecan_config():
    # Set up the pecan configuration
    filename = api_config.__file__.replace('.pyc', '.py')   # api/config.py
    return pecan.configuration.conf_from_file(filename)


def setup_app(pecan_config=None, extra_hooks=None):

    app_conf = get_pecan_config()

    app_hooks = [
        hooks.ContextHook(),
    ]

    app = pecan.make_app(
        app_conf.app.root,
        static_root=app_conf.app.static_root,
        template_path=app_conf.app.template_path,
        debug=CONF.api.pecan_debug,
        force_canonical=getattr(app_conf.app, 'force_canonical', True),
        hooks=app_hooks,
        guess_content_type_from_ext=False
    )

    return app


def load_app():
    cfg_file = None
    cfg_path = cfg.CONF.api_paste_config
    if not os.path.isabs(cfg_path):
        cfg_file = CONF.find_file(cfg_path)
    elif os.path.exists(cfg_path):
        cfg_file = cfg_path

    if not cfg_file:
        raise cfg.ConfigFilesNotFoundError([cfg.CONF.api_paste_config])
    LOG.info("Full WSGI config used: %s", cfg_file)
    appname = "pecan_demo+{}".format(cfg.CONF.auth_strategy)
    LOG.info("pecan_demo api with '%s' auth type will be loaded.",
             cfg.CONF.auth_strategy)
    return deploy.loadapp("config:" + cfg_file, name=appname)


def build_wsgi_app(argv=None):
    service.prepare_service()
    return load_app()


def app_factory(global_config, **local_conf):
    return setup_app()


if __name__ == '__main__':
    """
    python app.py --config-file test.conf
    """
    import sys

    cfg.CONF(sys.argv[1:])
    print("the test %s" % cfg.CONF.api.host_ip)
    print("the test %s" % cfg.CONF.DEFAULT.test)

    pass
