#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 13:46
# @Author   :shana
# @File     :__init__.py
from pecan import rest

from pecan_demo.api.v1.controllers import demo as demo_api


class V1Controller(rest.RestController):
    """API version 1 controller.

    """

    # demo = demo_api.DemoController()
    demo = demo_api.TestController()