#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 11:31
# @Author   :shana
# @File     :base.py
from oslo_policy import policy

RULE_ADMIN_OR_OWNER = 'rule:admin_or_owner'
ROLE_ADMIN = 'role:admin'
UNPROTECTED = ''

rules = [
    policy.RuleDefault(
        name='context_is_admin',
        check_str='role:admin'),
    policy.RuleDefault(
        name='admin_or_owner',
        check_str='is_admin:True or tenant:%(tenant_id)s'),
    policy.RuleDefault(
        name='default',
        check_str=UNPROTECTED)
]


def list_rules():
    return rules
