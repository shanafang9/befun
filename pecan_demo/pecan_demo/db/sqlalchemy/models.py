#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/18 15:38
# @Author   :shana
# @File     :models.py
import sqlalchemy
from sqlalchemy.ext import declarative
from oslo_db.sqlalchemy import models

Base = declarative.declarative_base()


class Demo(Base, models.ModelBase):
    """Demo"""
    __table_args__ = {'mysql_charset': "utf8",
                      'mysql_engine': "InnoDB"}
    __tablename__ = 'demo'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)  # 自增id
    demo_id = sqlalchemy.Column(sqlalchemy.String(40),
                                nullable=False,
                                unique=True)  # uuid
    desc = sqlalchemy.Column(sqlalchemy.Text(),
                             nullable=True)  # 描述
    name = sqlalchemy.Column(sqlalchemy.String(255),
                             nullable=False)  # 名称

    create_dt = sqlalchemy.Column(sqlalchemy.DateTime,
                                  nullable=False)
    update_dt = sqlalchemy.Column(sqlalchemy.DateTime,
                                  nullable=False)
    del_flag = sqlalchemy.Column(sqlalchemy.String(10),
                                 nullable=True)

    def __repr__(self):
        return ('<Demo[{name}]: '
                'demo_id={demo_id}>').format(
            name=self.name,
            demo_id=self.demo_id)

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            if c.name == 'id':
                d[c.name] = str(self[c.name])
            elif c.name == 'del_flag':
                continue
            else:
                d[c.name] = self[c.name]
        return d
