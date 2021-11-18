#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/18 14:10
# @Author   :shana
# @File     :__init__.py
from oslo_config import cfg
from oslo_db.sqlalchemy import session

_FACADE = None


def _create_facade_lazily():
    global _FACADE
    if _FACADE is None:
        _FACADE = session.EngineFacade.from_config(cfg.CONF, sqlite_fk=True)
    return _FACADE


def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session(**kwargs):
    facade = _create_facade_lazily()
    return facade.get_session(**kwargs)
