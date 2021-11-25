#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/18 15:37
# @Author   :shana
# @File     :api.py
import datetime
import sqlalchemy


from oslo_db import exception
from oslo_db.sqlalchemy import utils
from oslo_utils import uuidutils

from pecan_demo import db
from pecan_demo.db.sqlalchemy import migration, models
from pecan_demo.db import api


def get_backend():
    return DBAPIManager


class Demo(api.Demo):

    def get_demo(self, _uuid):
        """Return a field object."""
        session = db.get_session()
        try:
            q = utils.model_query(
                models.Demo,
                session)
            q = q.filter(models.Demo.demo_id == _uuid,
                         models.Demo.del_flag != '1')
            demo = q.one()
            return demo
        except sqlalchemy.orm.exc.NoResultFound as e:
            raise api.NoSuchDemo("")
        except sqlalchemy.orm.exc.MultipleResultsFound:
            raise api.ApiDemoError()

    def create_demo(self, name, desc='None', del_flag='0'):
        """Create a new demo."""
        session = db.get_session()
        now = datetime.datetime.now()
        with session.begin():
            demo_db = models.Demo(
                demo_id=uuidutils.generate_uuid(),
                name=name,
                desc=desc,
                create_dt=now,
                update_dt=now,
                del_flag=del_flag)
            session.add(demo_db)
        return demo_db


"""
将 alembic 迁移数据局、以及 migration.py 迁移脚本 以模块形式分开便于后续扩展

"""


class DBAPIManager(object):

    @staticmethod
    def get_demo():
        return Demo()

    @staticmethod
    def get_migration():
        return migration
