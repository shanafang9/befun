#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/12/14 15:30
# @Author   :shana
# @File     :_notification.py
import cotyledon
from cotyledon import oslo_config_glue

from pecan_demo.manager.message_manager import MessageManager
from pecan_demo import notification
from pecan_demo import service


def main():
    conf = service.prepare_service()
    sm = cotyledon.ServiceManager()
    # cpuNum = multiprocessing.cpu_count() or 1
    cpuNum = 1
    # 根据性能需求调整 worker 数
    workerNum = min(4, cpuNum)
    message_mgr = MessageManager()
    for i in ['nova', 'neutron', 'cinder']:
        sm.add(notification.NotificationServer, workers=workerNum, args=(conf, i, message_mgr))
        oslo_config_glue.setup(sm, conf)
    print "rabbitMQ listener is started..."
    sm.run()


if __name__ == '__main__':
    main()