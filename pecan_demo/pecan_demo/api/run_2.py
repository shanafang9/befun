#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/18 9:32
# @Author   :shana
# @File     :run_2
from wsgiref import simple_server

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config
from pycallgraph import GlobbingFilter

from pecan_demo.api import app

application = app.build_wsgi_app(argv=[])


def main():
    serve = simple_server.make_server('0.0.0.0', 8887, application)
    serve.serve_forever()


if __name__ == '__main__':
    config = Config()
    # 关系图中需要包括的函数
    config.trace_filter = GlobbingFilter(include=[
        '*',  # 所有
    ])

    # 关系图中需要过滤的函数
    config.trace_filter = GlobbingFilter(exclude=[
        'pycallgraph.*',  # 所有
    ])

    graphviz = GraphvizOutput()
    graphviz.output_file = 'graph.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
