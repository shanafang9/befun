# 目的

1. 介绍, 基于python-web框架 Pecan 搭建的基础架构
2. OpenStack 常用的基础组件
3. 再现有基础组件上实现自定义的需求及功能



项目初始结构

$ tree -L 4
.
|-- README.md
|-- etc
|   |-- oslo-config-generator
|   |   `-- sit
|   |       `-- pecan_demo.conf
|   |-- pecan_api
|   `-- pecan_test_api
|       `-- api_paste.ini
|-- pecan_demo
|   |-- api
|   |   |-- __init__.py
|   |   `-- v1
|   |       |-- __init__.py
|   |       |-- controllers
|   |       `-- datamodels
|   |-- cli
|   |   `-- __init__.py
|   |-- common
|   |   `-- __init__.py
|   |-- db
|   |   `-- __init__.py
|   `-- service.py
|-- setup.cfg
`-- setup.py




keystonemiddleware==7.0.1