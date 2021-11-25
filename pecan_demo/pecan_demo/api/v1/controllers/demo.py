#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 13:46
# @Author   :shana
# @File     :demo.py
import six
from oslo_log import log as logging  # noqa
import pecan
from pecan import rest
import wsmeext.pecan as wsme_pecan

from pecan_demo.db import api as db_api
from pecan_demo.api.v1 import types as _types
from pecan_demo.api.v1.datamodels import demo as demo_schema


class DemoController(rest.RestController):

    @pecan.expose()
    def index(self):
        return 'DemoController'


class TestController(rest.RestController):

    def __init__(self):
        """
        oslo_db: Initialize the chosen DB API backend.
        """
        self._db = db_api.get_instance().get_demo()

    # @pecan.expose('json')
    @wsme_pecan.wsexpose(demo_schema.DemoModel,
                         _types.UuidType(),
                         status_code=200)
    def get(self, uuid):
        try:
            demo = self._db.get_demo(uuid)
            return demo_schema.DemoModel(**demo.as_dict())
        except Exception as e:
            pecan.abort(400, six.text_type(e))
            pass
        # return 'get'

    @wsme_pecan.wsexpose(demo_schema.DemoModel,
                         body=demo_schema.DemoModel,
                         status_code=201)
    def post(self, demo_body):
        try:
            demo = self._db.create_demo(
                name=demo_body.name,
                desc=demo_body.desc)
            return demo_schema.DemoModel(**demo.as_dict())
        except Exception as e:
            pecan.abort(400, six.text_type(e))
        # return 'post'
