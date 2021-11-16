#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 11:27
# @Author   :shana
# @File     :__init__.py
import itertools

from pecan_demo.common.policies import base


def list_rules():
    return itertools.chain(
        base.list_rules(),
    )
