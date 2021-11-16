#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 10:32
# @Author   :shana
# @File     :hooks.py
from oslo_context import context
from pecan import hooks

from pecan_demo.common import policy
from pecan_demo import messaging


# class RPCHook(hooks.PecanHook):
#     def __init__(self):
#         self._rpc_client = messaging.get_client()
#
#     def before(self, state):
#         state.request.rpc_client = self._rpc_client


class ContextHook(hooks.PecanHook):
    def on_route(self, state):
        headers = state.request.headers

        roles = headers.get('X-Roles', '').split(',')
        is_admin = policy.check_is_admin(roles)

        creds = {
            'user_id': headers.get('X-User-Id', ''),
            'tenant': headers.get('X-Tenant-Id', ''),
            'auth_token': headers.get('X-Auth-Token', ''),
            'is_admin': is_admin,
            'roles': roles,
            "user_name": headers.get('X-User-Name', ''),
            "project_name": headers.get('X-Project-Name', ''),
            "domain": headers.get('X-User-Domain-Id', ''),
            "domain_name": headers.get('X-User-Domain-Name', ''),
        }

        state.request.context = context.RequestContext(**creds)