#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/12/14 14:37
# @Author   :shana
# @File     :notification
import random

import cotyledon
import time
import json
import traceback
import pika
from pika.exceptions import ConnectionClosed, ChannelClosed

from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class NotificationServer(cotyledon.Service):
    """Custom message listening service"""

    def __init__(self, worker_id, conf, exchange, message_mgr):
        super(NotificationServer, self).__init__(worker_id)
        self.conf = conf
        self.exchange = exchange  # 'nova'
        self.message_mgr = message_mgr
        self.connection = None
        self.channel = None

    def reconnect(self):
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()

            # 适配集群
            tmp = self.conf.self_transport_url.split('//')
            if len(tmp) > 2:
                # 多节点
                url_list = ['amqp://'+i for i in tmp[1].split(';')]
                all_endpoints = [pika.URLParameters(url) for url in url_list]
                random.shuffle(all_endpoints)
                for parameters in all_endpoints:
                    try:
                        self.connection = pika.BlockingConnection(parameters)
                    except Exception as ex:
                        print str(ex)
                    else:
                        break
            else:
                # 单节点
                parameters = pika.URLParameters(self.conf.self_transport_url)   # URLParameters 无法解析集群配置信息
                self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

            result = self.channel.queue_declare(queue='queue_{}'.format(self.exchange), exclusive=True)
            queue_name = result.method.queue
            # 针对不同组件绑定不同 routing_key
            if self.exchange == 'cinder':
                # exchange = 'openstack'
                exchange = 'cinder'
                routing_key = 'cinder-scheduler'
            else:
                exchange = self.exchange
                routing_key = 'notifications.*'
            self.channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
            self.channel.basic_consume(queue=queue_name, on_message_callback=self.consumer_callback, auto_ack=True)
        except Exception as e:
            LOG.error('reconnect: ' + str(e))
            print e

    def consumer_callback(self, ch, method, properties, body):
        print 'exchange: ', self.exchange
        LOG.info('exchange: ' + self.exchange)
        try:
            if self.exchange == 'cinder':
                self.message_mgr.mq_message_listener_cinder(body)
            else:
                self.message_mgr.mq_message_listener(body)
        except Exception as e:
            LOG.error('consumer_callback: ' + traceback.format_exc())
        # print " %r:%r " % (method.routing_key, body)

    def start_consumer(self):
        while True:
            try:
                self.reconnect()
                self.channel.start_consuming()
            except ConnectionClosed as e:
                self.reconnect()
                time.sleep(1)
            except ChannelClosed as e:
                self.reconnect()
                time.sleep(1)
            except Exception as e:
                self.reconnect()
                time.sleep(1)

    def run(self):
        self.start_consumer()
