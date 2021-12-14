#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time     :2021/12/14 15:16
# @Author   :shana
# @File     :nova_msg.py


def get_action_and_stage(msg, event_type_array):
    if event_type_array[3] == 'prep' or event_type_array[3] == 'confirm':
        msg['action'] = event_type_array[2] + '_' + event_type_array[3]
        msg['stage'] = event_type_array[4]
    else:
        msg['action'] = event_type_array[2]
        msg['stage'] = event_type_array[3]


def nova_formatter(msg, event_type_array):
    """Parsing nova RabbitMQ messages.

    :param msg: Original message body
    :param event_type_array: Array of event types
    """
    message = {}
    if event_type_array[2] == 'snapshot':
        message['resource_type'] = 'image'
        message['action'] = 'create'
        message['stage'] = event_type_array[3]
    else:
        message['resource_type'] = 'instance'
        get_action_and_stage(message, event_type_array)
    message['resource_id'] = msg['payload']['instance_id']
    message['user_id'] = msg['_context_user_id']
    message['resource_name'] = msg['payload']['display_name']
    message['resource_state'] = msg['payload']['state']
    message['request_id'] = msg['_context_request_id']
    return message
