#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/18 16:45
# @Author   :shana
# @File     :dbsync.py
from oslo_config import cfg
from stevedore import extension

from pecan_demo import config  # noqa
from pecan_demo.db import api as db_api
from pecan_demo import service

CONF = cfg.CONF


class ModuleNotFound(Exception):
    def __init__(self, name):
        self.name = name
        super(ModuleNotFound, self).__init__(
            "Module %s not found" % name)


class MultipleModulesRevisions(Exception):
    def __init__(self, revision):
        self.revision = revision
        super(MultipleModulesRevisions, self).__init__(
            "Can't apply revision %s to multiple modules." % revision)


class DBCommand(object):

    def __init__(self):
        self.rating_models = {}

    def get_module_migration(self, name):
        if name == 'pecan_demo':
            mod_migration = db_api.get_instance().get_migration()
        else:
            raise ModuleNotFound(name)
        return mod_migration

    def get_migrations(self, name=None):
        if not name:
            migrations = []
            migrations.append(self.get_module_migration('pecan_demo'))
            for model in self.rating_models.values():
                migrations.append(model.get_migration())
            return migrations
        else:
            return [self.get_module_migration(name)]

    def check_revsion(self, revision):
        revision = revision or 'head'
        if revision not in ('base', 'head'):
            raise MultipleModulesRevisions(revision)

    def _version_change(self, cmd):
        revision = CONF.command.revision
        module = CONF.command.module
        if not module:
            self.check_revsion(revision)
        migrations = self.get_migrations(module)
        for migration in migrations:
            func = getattr(migration, cmd)
            func(revision)

    def upgrade(self):
        self._version_change('upgrade')

    def revision(self):
        migration = self.get_module_migration(CONF.command.module)
        migration.revision(CONF.command.message, CONF.command.autogenerate)

    def stamp(self):
        migration = self.get_module_migration(CONF.command.module)
        migration.stamp(CONF.command.revision)

    def version(self):
        migration = self.get_module_migration(CONF.command.module)
        migration.version()


def add_command_parsers(subparsers):
    command_object = DBCommand()

    parser = subparsers.add_parser('upgrade')
    parser.set_defaults(func=command_object.upgrade)
    parser.add_argument('--revision', nargs='?')
    parser.add_argument('--module', nargs='?')

    parser = subparsers.add_parser('stamp')
    parser.set_defaults(func=command_object.stamp)
    parser.add_argument('--revision', nargs='?')
    parser.add_argument('--module', required=True)

    parser = subparsers.add_parser('revision')
    parser.set_defaults(func=command_object.revision)
    parser.add_argument('-m', '--message')
    parser.add_argument('--autogenerate', action='store_true')
    parser.add_argument('--module', required=True)

    parser = subparsers.add_parser('version')
    parser.set_defaults(func=command_object.version)
    parser.add_argument('--module', required=True)


command_opt = cfg.SubCommandOpt('command',
                                title='Command',
                                help='Available commands',
                                handler=add_command_parsers)

CONF.register_cli_opt(command_opt)


def main():
    service.prepare_service()
    CONF.command.func()


if __name__ == '__main__':
    main()
