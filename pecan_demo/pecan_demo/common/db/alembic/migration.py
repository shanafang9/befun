#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 11:33
# @Author   :shana
# @File     :migration.py
import os

import alembic
from alembic import config as alembic_config

ALEMBIC_INI_PATH = os.path.join(os.path.dirname(__file__), 'alembic.ini')


def load_alembic_config(repo_path, ini_path=ALEMBIC_INI_PATH):
    if not os.path.exists(repo_path):
        raise Exception('Repo path (%s) not found.' % repo_path)
    if not os.path.exists(ini_path):
        raise Exception('Ini path (%s) not found.' % ini_path)
    config = alembic_config.Config(ini_path)
    config.set_main_option('script_location', repo_path)
    return config


def upgrade(config, version):
    return alembic.command.upgrade(config, version or 'head')


def version(config):
    return alembic.command.current(config)


def revision(config, message='', autogenerate=False):
    """Creates template for migration.

    :param message: Text that will be used for migration title
    :type message: string
    :param autogenerate: If True - generates diff based on current database
                            state
    :type autogenerate: bool
    """
    return alembic.command.revision(config, message=message,
                                    autogenerate=autogenerate)


def stamp(config, revision):
    """Stamps database with provided revision.

    :param revision: Should match one from repository or head - to stamp
                        database with most recent revision
    :type revision: string
    """
    return alembic.command.stamp(config, revision=revision)
