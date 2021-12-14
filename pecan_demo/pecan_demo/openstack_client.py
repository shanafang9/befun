#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/12/14 14:55
# @Author   :shana
# @File     :openstack_client
import functools

from keystoneauth1.identity import v3
from keystoneauth1 import session
import novaclient
from novaclient import api_versions
from novaclient import client as nova_client
from cinderclient.v3 import client as cinder_client
from keystoneclient.v3 import client as ks_client
from oslo_log import log

DEFAULT_GROUP = "service_credentials"

LOG = log.getLogger(__name__)


def logged(func):
    @functools.wraps(func)
    def with_logging(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            LOG.exception(e)
            raise

    return with_logging


class Client(object):
    """A client which gets information via (python-novaclient|keystoneclient|cinderclient)."""

    def __init__(self, conf):
        """Initialize a nova|keystone|cinder client object."""
        creds = conf.service_credentials

        ks_session = self.get_session(creds)

        self.nova_client = nova_client.Client(
            version=api_versions.APIVersion('2.1'),
            session=ks_session,

            # nova adapter options
            region_name=creds.region_name,
            endpoint_type=creds.interface,
            service_type=conf.service_types.nova)

        self.ks_client = ks_client.Client(
            session=ks_session)

        # self.cinder_client = cinder_client.Client(
        #     session=ks_session)

    def get_session(self, creds):
        auth = v3.Password(username=creds.username,
                           password=creds.password,
                           project_name=creds.project_name,
                           user_domain_id=creds.user_domain_id,
                           project_domain_id=creds.project_domain_id,
                           auth_url=creds.auth_url)
        return session.Session(auth=auth)

    def _with_flavor_and_image(self, instances):
        flavor_cache = {}
        # image_cache = {}
        for instance in instances:
            self._with_flavor(instance, flavor_cache)

        return instances

    def _with_flavor(self, instance, cache):
        fid = instance.flavor['id']
        if fid in cache:
            flavor = cache.get(fid)
        else:
            try:
                flavor = self.nova_client.flavors.get(fid)
            except novaclient.exceptions.NotFound:
                flavor = None
            cache[fid] = flavor

        attr_defaults = [('name', 'unknown-id-%s' % fid),
                         ('vcpus', 0), ('ram', 0), ('disk', 0),
                         ('ephemeral', 0)]

        for attr, default in attr_defaults:
            if not flavor:
                instance.flavor[attr] = default
                continue
            instance.flavor[attr] = getattr(flavor, attr, default)

    @logged
    def instance_get_all_by_host(self, hostname, since=None):
        """Returns list of instances on particular host.

        If since is supplied, it will return the instances changed since that
        datetime. since should be in ISO Format '%Y-%m-%dT%H:%M:%SZ'
        """
        search_opts = {'host': hostname, 'all_tenants': True}
        if since:
            search_opts['changes-since'] = since
        return self._with_flavor_and_image(self.nova_client.servers.list(
            detailed=True,
            search_opts=search_opts))

    @logged
    def instance_get_all(self, since=None):
        """Returns list of all instances.

        If since is supplied, it will return the instances changes since that
        datetime. since should be in ISO Format '%Y-%m-%dT%H:%M:%SZ'
        """
        search_opts = {'all_tenants': True}
        if since:
            search_opts['changes-since'] = since
        return self.nova_client.servers.list(
            detailed=True,
            search_opts=search_opts)

    @logged
    def instance_get_all_new(self, since=None):
        """Returns list of all instances.

        If since is supplied, it will return the instances changes since that
        datetime. since should be in ISO Format '%Y-%m-%dT%H:%M:%SZ'
        """
        search_opts = {'all_tenants': True}
        if since:
            search_opts['changes-since'] = since
        tmp_list = self.nova_client.servers.list(
            detailed=True,
            search_opts=search_opts)
        result = {}
        for i in tmp_list:
            result[i.id] = i.name
        if not result:
            LOG.error('[nova] servers data fails to be obtained')
        return result

    @logged
    def flavor_get_all(self):
        result = {}
        flavor_list = self.nova_client.flavors.list()
        for i in flavor_list:
            result[i.id] = 'vcpus:{} ,ram:{} ,disk:{} '.format(i.vcpus, i.ram, i.disk)
        if not result:
            LOG.error('[nova] flavors data fails to be obtained')
        return result

    @logged
    def project_get_all(self):
        """Returns a list of all project information."""
        result = {}
        project_list = self.ks_client.projects.list()
        for i in project_list:
            result[i.id] = i.name
        if not result:
            LOG.error('[keystone] projects data fails to be obtained')
        return result

    @logged
    def user_get_all(self):
        """Returns a list of all user information."""
        result = {}
        project_list = self.ks_client.users.list()
        for i in project_list:
            result[i.id] = i.name
        if not result:
            LOG.error('[keystone] user data fails to be obtained')
        return result

    # @logged
    # def volume_get_all(self):
    #     search_opts = {'all_tenants': True}
    #     tmp_list = self.cinder_client.volumes.list(
    #         search_opts=search_opts)
    #     result = {}
    #     for i in tmp_list:
    #         result[i.id] = 'name:{} ,type:{}'.format(i.name, i.volume_type)
    #     if not result:
    #         LOG.error('[cinder] volumes data fails to be obtained')
    #     return result
