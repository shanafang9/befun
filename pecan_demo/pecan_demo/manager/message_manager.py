#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/12/14 15:14
# @Author   :shana
# @File     :message_manager.py
import json

from oslo_log import log as logging

from pecan_demo.manager.nova_msg import nova_formatter
from pecan_demo.manager.cinder_msg import cinder_formatter, cinder_formatter_2
from pecan_demo.constant import OpenStackResEventType as Op

LOG = logging.getLogger(__name__)


def switch_case(msg):
    switcher = {
        'compute.instance.resize.confirm.start': lambda msg: msg['payload']['tenant_id'],
        'compute.instance.resize.confirm.end': lambda msg: msg['payload']['tenant_id'],
        'image.delete': lambda msg: msg['payload']['owner'],
        'port.create.end': lambda msg: msg['payload']['port']['tenant_id'],
        'port.update.end': lambda msg: msg['payload']['port']['tenant_id'],
    }
    print 'switch_case', msg['event_type']
    LOG.info('switch_case' + msg['event_type'])
    return switcher.get(msg['event_type'], msg['_context_project_id'])


def switch_case_get_res_id(msg, event_type_array):
    switcher = {
        'compute': lambda msg: msg['payload']['instance_id'],
        'volume': lambda msg:
        msg['payload']['volume_id'] if event_type_array[0] == 'volume' else msg['payload']['snapshot_id'],
        'network': lambda msg: msg['payload']['network']['id'],  # 网络
        'subnet': lambda msg: msg['payload']['subnet']['id'],  # 子网
        'router': lambda msg: msg['payload']['router']['id'],  # 路由
        'floatingip': lambda msg: msg['payload']['floatingip']['id'],  # 公网IP
    }

    return switcher.get(event_type_array[0])(msg)


def switch_case_msg_handler(msg, event_type_array):
    switcher = {
        'compute': nova_formatter,
        # 'volume': cinder_formatter,
        # 'network': neutron_formatter,  # 网络
        # 'subnet': neutron_formatter,  # 子网
        # 'router': neutron_formatter,  # 路由
        # 'floatingip': neutron_formatter,  # 公网IP
    }
    print 'switch_case_msg_handler: ', msg['event_type']
    LOG.info('switch_case_msg_handler: ' + msg['event_type'])
    return switcher.get(event_type_array[0], None)


class MessageManager(object):
    """事件处理"""

    def __init__(self):
        self.ignore_list = [
            'compute.instance.update',
            'compute.instance.exists',
            'scheduler.select_destinations.start',
            'scheduler.select_destinations.end',
            'image.update',
            'image.activate',
            'image.upload',
            'image.create',
            'image.prepare',
        ]
        self.error_list = [
            'external_instance_event',
            'compute.instance.create.error',
        ]
        # 进行其他数据处理 初始化操作
        # self._db = db_api.get_instance()...

    def get_listener_name(self, msg):
        if msg['event_type'].find('orchestration.stack') >= 0:
            return msg['_context_tenant_id']
        return switch_case(msg)

    def _filter_msg_type(self, msg, type_field='event_type'):
        msg_content = json.loads(str(msg))
        if msg_content['oslo.version'] == '2.0':
            msg_content = json.loads(msg_content['oslo.message'])
        if not self.if_effective_msg(msg_content[type_field]):
            # 非资源创建消息，不做处理
            return None, None
        msg_type = msg_content[type_field]
        LOG.info('all: ' + msg_type)
        print 'all: ', msg_type

        return msg_content, msg_type

    def mq_message_listener_cinder(self, msg):
        msg_content, msg_type = self._filter_msg_type(msg, type_field='method')
        if msg_type:
            formatted_msg = cinder_formatter_2(msg_content)
            if formatted_msg and formatted_msg['request_id']:
                print 'formatted_msg: ', formatted_msg
                LOG.info('cinder formatted_msg: ' + str(formatted_msg))
                # todo 数据处理 pass
            else:
                LOG.error('mq_message_listener_cinder: %s' % msg)
        else:
            # cinder 无用消息不做记录
            pass

    def mq_message_listener(self, msg):
        msg_content, msg_type = self._filter_msg_type(msg)
        if not msg_content:
            # 非资源创建消息，不做处理
            return
        # 异常捕获
        if self.is_error_msg(msg_type):
            error_msg = msg_content['payload']['exception']
            try:
                request_id = msg_content['_context_request_id']
                print 'error_msg: ', error_msg
                LOG.info('error_msg: ' + error_msg)
                # todo 数据处理 pass
            except Exception as e:
                pass
            return

        if self.is_ignored_msg(msg_type):
            print "ignored: ", msg_type
            LOG.info('ignored: ' + msg_type)
            return
        listener = self.get_listener_name(msg_content)  # 获取项目信息
        # LOG.info('tmp formatted_msg: ' + str(msg_content))
        formatted_msg = self.msg_formatter(msg_content)
        if formatted_msg:
            print 'formatted_msg: ', formatted_msg
            LOG.info('mq_message_listener other formatted_msg: ' + str(formatted_msg))
            # todo 数据处理

    def msg_formatter(self, msg):
        """解析 notifications.* 类型消息 """
        ret = None
        event_type_array = msg['event_type'].split('.')
        _tmp_func = switch_case_msg_handler(msg, event_type_array)
        if _tmp_func:
            ret = _tmp_func(msg, event_type_array)
        return ret

    def if_effective_msg(self, msg_type):
        return bool(Op.CREATE in msg_type)

    def is_ignored_msg(self, msg_type):
        return bool(msg_type in self.ignore_list)

    def is_error_msg(self, msg_type):
        return bool(msg_type in self.error_list)
