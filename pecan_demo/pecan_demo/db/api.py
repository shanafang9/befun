#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/18 14:12
# @Author   :shana
# @File     :api.py
import abc
import six

from oslo_config import cfg
from oslo_db import api as db_api

_BACKEND_MAPPING = {'sqlalchemy': 'pecan_demo.db.sqlalchemy.api'}
IMPL = db_api.DBAPI.from_config(cfg.CONF,
                                backend_mapping=_BACKEND_MAPPING,
                                lazy=True)

"""
get_instance 用于获取 sqlalchemy 实例化 db 对象
"""


def get_instance():
    """Return a DB API instance."""
    return IMPL


"""
通过 abc 模块定义抽象基类
    1. 代码可读性更高，abc基类只用作集成，不涉及实例化，所以不会攘括
        具体的代码实现，更简洁易读
    2. 便于后续扩展(OpenStack 的所有组件的各项操作都有很强的兼容性，
        例如数据存储(storage)，以 gnocchi 为例，它适配了 swift、ceph、
        file、s3、redis 5种；但是基础数据操作还是 CURD 方法的定义是
        能够复用或参考的
"""


@six.add_metaclass(abc.ABCMeta)
class Demo(object):
    """Base class for demo managing"""

    @abc.abstractmethod
    def get_demo(self, _uuid):
        """Return a field object."""

    # @abc.abstractmethod
    # def list_demos(self):
    #     """Return an detail list fo every demo."""

    @abc.abstractmethod
    def create_demo(self, name, desc, del_flag):
        """Create a new demo."""

    # @abc.abstractmethod
    # def update_demo(self, uuid):
    #     """Update a demo."""

    # @abc.abstractmethod
    # def delete_demo(self, uuid):
    #     """delete a demo."""


"""
这里定义了三种异常

BaseDemoError
    针对 demo 模块预留的全局异常，尽量减少 Exception 的直接操作，便于模块级日志定位

ApiDemoError
    仅共 controller(视图) 层使用，封装视图层所有未单独定义的报错信息 "raise ApiDemoError()"

NoSuchDemo
    针对 ORM 层常见报错定义，资源查询不到
"""


class BaseDemoError(Exception):
    """Base class for Demo errors."""


class ApiDemoError(BaseDemoError):
    """Base class for api side errors."""


class NoSuchDemo(ApiDemoError):
    """Raised when the demo doesn't exist."""

    def __init__(self, uuid=None):
        super(NoSuchDemo, self).__init__(
            "No demo for search: %s" % uuid)
        self.uuid = uuid
