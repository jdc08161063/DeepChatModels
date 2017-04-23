#!/usr/bin/env python3

"""db_migrate.py: generates a database migration.

Example; To generate migration:
    Command:    ./db_migrate.py
    Output:     New migration saved as db_repository/versions/001_migration.py
                Current database version: 1

A migration is any change to structure of the app database.

SQLAlchemy-migrate creates a migration by comparing the structure
of the database (obtained in our case from file app.db) against
the structure of our models (obtained from file app/models.py).

Never attempt to migrate your database without having a backup,
in case something goes wrong.

Also never run a migration for the first time on a production database,
always make sure the migration works correctly on a development database.
"""

from imp import new_module
from migrate.versioning import api
from deepchat import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


v           = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration   = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v + 1))
tmp_module  = new_module('old_model')
old_model   = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

exec(old_model, tmp_module.__dict__)
script      = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
                                               SQLALCHEMY_MIGRATE_REPO,
                                               tmp_module.meta,
                                               db.metadata)
open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))
