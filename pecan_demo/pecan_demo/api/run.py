#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 11:01
# @Author   :shana
# @File     :run.py
from wsgiref import simple_server
from pecan_demo.api import app
# import pdb
# pdb.set_trace()
application = app.build_wsgi_app(argv=[])

# print(type(application))


if __name__ == '__main__':
    serve = simple_server.make_server('0.0.0.0', 8887, application)
    serve.serve_forever()
