#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/11/16 10:51
# @Author   :shana
# @File     :root.py
from oslo_config import cfg
import pecan
from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from pecan_demo.api.v1 import controllers as v1_api

CONF = cfg.CONF
CONF.import_opt('port', 'pecan_demo.api.app', 'api')


class APILink(wtypes.Base):
    """API link description.

    """

    type = wtypes.text
    """Type of link."""

    rel = wtypes.text
    """Relationship with this link."""

    href = wtypes.text
    """URL of the link."""

    @classmethod
    def sample(cls):
        version = 'v1'
        sample = cls(
            rel='self',
            type='text/html',
            href='http://127.0.0.1:{port}/{id}'.format(
                port=CONF.api.port,
                id=version))
        return sample


class APIMediaType(wtypes.Base):
    """Media type description.

    """

    base = wtypes.text
    """Base type of this media type."""

    type = wtypes.text
    """Type of this media type."""

    @classmethod
    def sample(cls):
        sample = cls(
            base='application/json',
            type='application/vnd.openstack.pecan_demo-v1+json')
        return sample


VERSION_STATUS = wtypes.Enum(wtypes.text, 'EXPERIMENTAL', 'STABLE')


class APIVersion(wtypes.Base):
    """API Version description.

    """

    id = wtypes.text
    """ID of the version."""

    status = VERSION_STATUS
    """Status of the version."""

    updated = wtypes.text
    "Last update in iso8601 format."

    links = [APILink]
    """List of links to API resources."""

    media_types = [APIMediaType]
    """Types accepted by this API."""

    @classmethod
    def sample(cls):
        version = 'v1'
        updated = '2021-05-28T09:00:00'
        links = [APILink.sample()]
        media_types = [APIMediaType.sample()]
        sample = cls(id=version,
                     status='STABLE',
                     updated=updated,
                     links=links,
                     media_types=media_types)
        return sample


class RootController(rest.RestController):
    """Root REST Controller exposing versions of the API.

    """

    v1 = v1_api.V1Controller()

    @wsme_pecan.wsexpose([APIVersion])
    def index(self):
        """Return the version list

        """
        # TODO(sheeprine): Maybe we should store all the API version
        # informations in every API modules
        ver1 = APIVersion(
            id='v1',
            status='EXPERIMENTAL',
            updated='2021-11-16T09:00:00',
            links=[
                APILink(
                    rel='self',
                    href='{scheme}://{host}/v1'.format(
                        scheme=pecan.request.scheme,
                        host=pecan.request.host,
                    )
                )
            ],
            media_types=[]
        )

        versions = []
        versions.append(ver1)

        return versions
