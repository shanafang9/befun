#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/12/14 15:20
# @Author   :shana
# @File     :constant.py


class OpenStackResEventType(object):
    """OpenStack resource state constant。"""
    CREATE = 'create'
    START = 'start'
    END = 'end'
    ERROR = 'error'
