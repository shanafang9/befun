#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/18 15:38
# @Author   :shana
# @File     :migration.py
import os

from pecan_demo.common.db.alembic import migration

ALEMBIC_REPO = os.path.join(os.path.dirname(__file__), 'alembic')


def upgrade(revision):
    config = migration.load_alembic_config(ALEMBIC_REPO)
    return migration.upgrade(config, revision)


def version():
    config = migration.load_alembic_config(ALEMBIC_REPO)
    return migration.version(config)


def revision(message, autogenerate):
    config = migration.load_alembic_config(ALEMBIC_REPO)
    return migration.revision(config, message, autogenerate)


def stamp(revision):
    config = migration.load_alembic_config(ALEMBIC_REPO)
    return migration.stamp(config, revision)