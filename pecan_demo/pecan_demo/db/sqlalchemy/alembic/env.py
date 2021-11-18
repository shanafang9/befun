from pecan_demo.common.db.alembic import env  # noqa
from pecan_demo.db.sqlalchemy import models

target_metadata = models.Base.metadata
version_table = 'pecan_demo_alembic'


env.run_migrations_online(target_metadata, version_table)