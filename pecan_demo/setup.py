# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='pecan_demo',
    version='0.1',
    packages=find_packages(),
    package_data={
        'pecan_demo': [
            'common/db/alembic/alembic.ini'
            'db/sqlalchemy/alembic',
            'db/sqlalchemy/alembic/versions',
            'db/sqlalchemy/alembic/versions/c6040f85e16e_initial_migration.py',
            'db/sqlalchemy/alembic/env.py',
            'db/sqlalchemy/alembic/README',
            'db/sqlalchemy/alembic/script.py.mako',
        ],
    }
)