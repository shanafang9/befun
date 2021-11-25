# -*- coding: utf-8 -*-

import setuptools

try:
    import multiprocessing  # noqa
except ImportError:
    pass

setuptools.setup(
    setup_requires=['pbr>=1.8'],
    pbr=True,
    package_data={
        'pecan_demo': [
            'common/db/alembic/alembic.ini',
            'db/sqlalchemy/alembic',
            'db/sqlalchemy/alembic/version',
            'db/sqlalchemy/alembic/version/fe92e865ca17_init.py',
            'db/sqlalchemy/alembic/env.py',
            'db/sqlalchemy/alembic/README',
            'db/sqlalchemy/alembic/script.py.mako',
        ]
    }
)
