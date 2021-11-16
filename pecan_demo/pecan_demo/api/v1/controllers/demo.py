#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 13:46
# @Author   :shana
# @File     :demo.py
from oslo_log import log as logging
import pecan
from pecan import rest


class DemoController(rest.RestController):

    @pecan.expose()
    def index(self):
        return 'DemoController'
