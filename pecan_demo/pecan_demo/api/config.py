#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 10:31
# @Author   :shana
# @File     :config.py

from pecan_demo import config  # noqa


# Pecan Application Configurations
app = {
    'root': 'pecan_demo.api.root.RootController',    # 视图根节点
    'modules': ['pecan_demo.api'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/templates',
    'debug': False,
    'enable_acl': True,
    'acl_public_routes': ['/', '/v1'],
}