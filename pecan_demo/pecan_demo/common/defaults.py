#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 11:28
# @Author   :shana
# @File     :defaults.py
from oslo_middleware import cors


def set_config_defaults():
    """This method updates all configuration default values."""
    set_cors_middleware_defaults()


def set_cors_middleware_defaults():
    """Update default configuration options for oslo.middleware."""
    cors.set_defaults(
        allow_headers=['X-Auth-Token',
                       'X-Identity-Status',
                       'X-Roles',
                       'X-Service-Catalog',
                       'X-User-Id',
                       'X-Tenant-Id',
                       'X-OpenStack-Request-ID'],
        expose_headers=['X-Auth-Token',
                        'X-Subject-Token',
                        'X-Service-Token',
                        'X-OpenStack-Request-ID'],
        allow_methods=['GET',
                       'PUT',
                       'POST',
                       'DELETE',
                       'PATCH'])