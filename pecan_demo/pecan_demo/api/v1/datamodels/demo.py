#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/19 16:31
# @Author   :shana
# @File     :demo.py
import datetime

from wsme import types as wtypes
from pecan_demo.api.v1 import types as ck_types


class DemoModel(wtypes.Base):
    """Demo model"""

    id = wtypes.text
    """text of the demo id."""
    demo_id = wtypes.wsattr(ck_types.UuidType(), mandatory=False)
    """UUID of the demo demo_id."""
    desc = wtypes.wsattr(wtypes.text, mandatory=False)
    """text of the demo desc."""
    name = wtypes.wsattr(wtypes.text, mandatory=False)
    """text of the demo name."""

    create_dt = datetime.datetime
    """datetime of the demo create_dt."""
    update_dt = datetime.datetime
    """datetime of the demo update_dt."""
    del_flag = wtypes.text
    """text of the demo del_flag."""

    def __init__(self, id=None, demo_id=None, desc=None, name=None,
                 create_dt=None, update_dt=None, del_flag=None):
        self.id = id
        self.demo_id = demo_id
        self.desc = desc
        self.name = name

        self.create_dt = create_dt
        self.update_dt = update_dt
        self.del_flag = del_flag

    @classmethod
    def sample(cls):
        sample = cls(id='1',
                     demo_id='1d39e2e4-edd3-4997-a849-34a258798679',
                     desc='sample desc',
                     name='instance',
                     create_dt=datetime.datetime(2021, 6, 3, 17),
                     update_dt=datetime.datetime(2021, 6, 3, 17),
                     del_flag='0')
        return sample


class DemoCollectionModel(wtypes.Base):
    """A list of demo."""

    demos = [DemoModel]

    @classmethod
    def sample(cls):
        sample = DemoModel.sample()
        return cls(demos=[sample])
