#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/12/9 14:18
# @Author   :shana
# @File     :demo
from oslo_policy import policy

from pecan_demo.common.policies import base

demo_policies = [
    policy.DocumentedRuleDefault(
        name='demo:get_demo',
        check_str=base.UNPROTECTED,
        description='Return a demo.',
        operations=[{'path': '/v1/demo',
                     'method': 'GET'}]
    ),
    policy.DocumentedRuleDefault(
        name='demo:create_demo',
        check_str=base.ROLE_ADMIN,
        description='Create a new demo.',
        operations=[{'path': '/v1/demo',
                     'method': 'POST'}]
    ),
]
