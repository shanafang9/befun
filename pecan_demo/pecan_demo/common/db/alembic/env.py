#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 11:32
# @Author   :shana
# @File     :env.py
from logging import config as log_config

from alembic import context

from pecan_demo import db

config = context.config
log_config.fileConfig(config.config_file_name)


def run_migrations_online(target_metadata, version_table):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    :param target_metadata: Model's metadata used for autogenerate support.
    :param version_table: Override the default version table for alembic.
    """
    engine = db.get_engine()
    with engine.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata,
                          version_table=version_table)
        with context.begin_transaction():
            context.run_migrations()