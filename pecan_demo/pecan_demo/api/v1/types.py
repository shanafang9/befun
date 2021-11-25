#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/19 16:32
# @Author   :shana
# @File     :types.py
from oslo_utils import uuidutils
from wsme import types as wtypes


class UuidType(wtypes.UuidType):
    """A simple UUID type."""
    basetype = wtypes.text
    name = 'uuid'

    @staticmethod
    def validate(value):
        if not uuidutils.is_uuid_like(value):
            raise ValueError("Invalid UUID, got '%s'" % value)
        return value
