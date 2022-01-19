
[TOC]

# 前言

#### 内容主要用作个人学习总结，如有描述错误，欢迎指明

[**Pecan官方文档**](https://pecan.readthedocs.io/en/latest/index.html)
[**急速上手**](https://my.oschina.net/alazyer/blog/1555943)
<br>

涉及知识点
- Web: Pecan + Paste_Deployment
- 配置文件: oslo.config
- 入参校验: wsme
- 中间件: keystone_middleware
- ORM: SQLAlchemy
- 数据迁移: alembic

<br>
<br>

# 1

<br>

# 服务入口

接触过 OpenStack 的人都知道它有很多组件以及很多版本(这里以 cloudkitty-rocky 版为主)，在看组件的源码时，通常会以项目的 **setup.cfg** 文件入手<br>
如下所示:

![nova-rocky](https://images.cnblogs.com/cnblogs_com/blogs/695346/galleries/2062349/o_211115025014_nova-rocky-setup_cfg.png "nova-rocky-setup.cfg")
![cloudkitty-rocky-1](https://images.cnblogs.com/cnblogs_com/blogs/695346/galleries/2062349/o_211115025005_cloudkitty-rocky-1.png "cloudkitty-rocky-wsgi-app")


*PS：如果看不懂，请查看 [pbr 打包简介](https://www.cnblogs.com/CaesarLinsa/p/pbr.html)，链接的文章会大致讲解 setup.cfg 文件的构成以及相关 关键字的含义*

**先看** "**etc/nova/api-paste.ini**" 这一行，之前随笔有提到过，OpenStack-API 的整体结构有一个变化很大的地方

```
    1.Paste + PasteDeploy + Routes + WebOb
    2.Pecan (+Paste)

对比核心组件(nova) 和 新增组件(cloudkitty)的源码能发现， 路由映射相关的旧代码，在新版本里几乎找不到
```

[Paste Deployment](http://blog.chinaunix.net/uid-20940095-id-4105407.html) 用于发现和配置WSGI Application和Server，它的主要体现就是 **api-paste.ini** 这个配置文件。通过它，我们可以找到服务的入口，如下所示
![cloudkitty-rocky-3](https://images.cnblogs.com/cnblogs_com/blogs/695346/galleries/2062349/o_211116095724_cloudkitty-api_paste_ini.png "cloudkitty-api_paste_ini")


<br>
<br>
<br>


# 服务加载


读过 setup.cfg 和 api_paste.ini ，可以发现启动服务有多种切入方式

## 方式1：定义 setup.cfg

### setup.cfg

```
[entry_points]
...
wsgi_scripts =
    cloudkitty-api = cloudkitty.api.app:build_wsgi_app

# "wsgi_scripts" 代表这是一个 wsgi 的可执行脚本；以上述代码为例子，在 Linux 环境安装时，会在 /usr/bin 下生成一个名为 "cloudkitty-api" 的可执行文件；具体效果，大家可以在部署 OpenStack 环境时验证与查看
```

### cloudkitty/api/app.py
```
def build_wsgi_app(argv=None):
    service.prepare_service()
    return load_app()

def load_app():
    cfg_file = cfg.CONF.api_paste_config
    ...
    appname = "cloudkitty+{}".format(cfg.CONF.auth_strategy)
    return deploy.loadapp("config:" + cfg_file, name=appname)

```


![cloudkitty-rocky-1](https://images.cnblogs.com/cnblogs_com/blogs/695346/galleries/2062349/o_211115034427_setup_cfg-build-wsgi-app.png "build-wsgi-app_1")


## 方式2：定义 api_paste.ini
<div style="height:auto !important;max-height:200px;overflow:scroll;overflow-x:hidden;">

### api_paste.ini
```
[app:ck_api_v1]
paste.app_factory = cloudkitty.api.app:app_factory
```
### cloudkitty/api/app.py
```
def app_factory(global_config, **local_conf):
    return setup_app()

def setup_app(pecan_config=None, extra_hooks=None):

    app_conf = get_pecan_config()
    storage_backend = storage.get_storage()

    app_hooks = [
        hooks.RPCHook(),
        hooks.StorageHook(storage_backend),
        hooks.ContextHook(),
    ]

    app = pecan.make_app(
        app_conf.app.root,
        static_root=app_conf.app.static_root,
        template_path=app_conf.app.template_path,
        debug=CONF.api.pecan_debug,
        force_canonical=getattr(app_conf.app, 'force_canonical', True),
        hooks=app_hooks,
        guess_content_type_from_ext=False
    )

    return app
```

</div>


<br>

![cloudkitty-rocky-2](https://images.cnblogs.com/cnblogs_com/blogs/695346/galleries/2062349/o_211115060013_cloudkitty-rocky-2.png "build-wsgi-app_2")

你跟随 "app" 的实例化过程去看，就会发现上述2种方式都指向了 "app_factory" ，都是在[构建 wsgi-application](https://www.cnblogs.com/ajianbeyourself/p/4430782.html)

```
def setip_app():
return pecan.make_app()

     ->
    # Instantiate the WSGI app by passing **kw onward
    app = Pecan(root, **kw)

        ->
        PecanBase.__call__()
        ...
        return state.response(environ, start_response)
```


<br>
<br>
<br>

# 构建组件 demo

OpenStack 相关的第三方包，一般会涉及到以下部分

    # 通用模块
    1. from oslo_config import cfg      # 在 /etc/nova/nova.conf 里的配置项，都会加载到 cfg 中
    2. from oslo_log import log         # web 项目都会有日志模块，openstack 造好的轮子，不用白不用，在 /etc/<name>/<name>.conf 配置日志路径(一般是 /var/log/<name>)
    3. import oslo_messaging            # 消息模块，所有和消息中间件打交道的方法，都会在这个模块中体现
    4. from oslo_policy import policy   # 与 keystone 配套使用的权限模块，可以细化接口的权限控制
    5. import oslo_utils

    # 其他组件依赖
    1. from keystonemiddleware import auth_token


***


# 2


[Pecan: quick_start](https://pecan.readthedocs.io/en/latest/quick_start.html)
本章节将构建整合&验证API


# 目录结构

### 第 1 层
```
$ tree -L 1
.
|-- README.md
|-- etc             # 存放本地配置文件，例如 *.conf、api_paste.ini 等
|-- libs            # 环境构建过程较难安装的依赖包 *.whl
|-- log             # 存放本地调试的日志
|-- pecan_demo      # 项目
|-- setup.cfg       # 安装： 声明式 配置文件
`-- setup.py        # 安装： python 执行脚本

4 directories, 3 files

```

### 第 2 层

<div style="height:auto !important;max-height:300px;overflow:scroll;overflow-x:hidden;">
</div>

```

|-- pecan_demo
|   |-- __init__.py
|   |-- __init__.pyc
|   |-- api                 # API 核心
|   |-- cli                 # 预留的 Linux command
|   |-- common              # 公共模块
|   |-- config.py           # 预留配置文件，供 cfg 使用
|   |-- config.pyc
|   |-- db                  # 存储模块
|   |-- messaging.py        # 消息队列相关函数处理及封装
|   |-- messaging.pyc
|   |-- service.py          # cfg 加载&初始化
|   |-- service.pyc
|   |-- version.py          # 项目版本信息(pbr.version_info)
|   `-- version.pyc

```


<br>
<br>
<br>

# 内部实现

### 接下来按加载顺序依次介绍


![pecan_demo 流程图](https://images.cnblogs.com/cnblogs_com/blogs/695346/galleries/2062349/o_211117055707_pecan_demo%E5%8A%A0%E8%BD%BD%E6%B5%81%E7%A8%8B%E5%9B%BE.png "pecan_demo 流程图")


### #1 定义启动文件
*debug用*

文件：pecan_demo/api/run.py
```
from wsgiref import simple_server
from pecan_demo.api import app
# import pdb
# pdb.set_trace()
application = app.build_wsgi_app(argv=[])

# print(type(application))


if __name__ == '__main__':
    serve = simple_server.make_server('0.0.0.0', 8887, application)
    serve.serve_forever()
```

### #2 配置 cfg

文件：etc/oslo-config-generator/dev/pecan_demo.conf
```
[DEFAULT]
api_paste_config = 'F:\***\pecan_demo\etc\pecan_test_api\api_paste.ini'
log_dir = F:\***\pecan_demo\log
auth_strategy = keystone

[database]
connection = mysql+pymysql://root:123456@localhost/pecan_demo
```

文件：pecan_demo/api/app.py
```
auth_opts = [
    cfg.StrOpt('api_paste_config',
               default="api_paste.ini",
               help="Configuration file for WSGI definition of API."),
    cfg.StrOpt('auth_strategy',
               choices=['noauth', 'keystone'],
               default='keystone',
               help=("The strategy to use for auth. Supports noauth and "
                     "keystone")),
]

# CONF.register_opts(auth_opts, group='DEFAULT')
CONF.register_opts(auth_opts)
```

所有 *.conf 里的配置项，都要在项目初始化时，在 cfg 里注册；oslo.config 相关的介绍网上太多了，不赘述 贴两个参考 [demo1](https://www.cnblogs.com/Security-Darren/p/3854797.html)、
[demo2](https://www.cnblogs.com/cxchanpin/p/7093931.html)


### #3 加载 cfg
文件：pecan_demo/service.py
```
def prepare_service(argv=None, config_files=None):
    if argv is None:
        argv = sys.argv                 # 命令行参数预留

    oslo_i18n.enable_lazy()             # 国际化模块
    log.register_options(cfg.CONF)      # 日志配置加载
    log.set_defaults()
    defaults.set_cors_middleware_defaults()

    # 配置解析(建议用 rpdb 断点调试这里，可以加深 oslo.config 模块的理解)
    cfg.CONF(argv[1:], project='pecan_demo', validate_default_values=True,
             version=version.version_info.version_string(),
             default_config_files=config_files)

    log.setup(cfg.CONF, 'pecan_demo')
    messaging.setup()
    return cfg.CONF
```



### #4 Pecan 初始化
文件：pecan_demo/api/app.py
```
from pecan_demo.api import config as api_config
from pecan_demo.api import hooks

def get_pecan_config():
    # Set up the pecan configuration
    filename = api_config.__file__.replace('.pyc', '.py')   # api/config.py
    return pecan.configuration.conf_from_file(filename)

def setup_app(pecan_config=None, extra_hooks=None):

    app_conf = get_pecan_config()

    app_hooks = [
        hooks.ContextHook(),    # Pecan钩子，程序有预加载的数据或驱动，可以放在这里
    ]

    app = pecan.make_app(
        app_conf.app.root,      # 视图的根节点
        static_root=app_conf.app.static_root,
        template_path=app_conf.app.template_path,
        debug=CONF.api.pecan_debug,
        force_canonical=getattr(app_conf.app, 'force_canonical', True),
        hooks=app_hooks,
        guess_content_type_from_ext=False
    )

    return app      # wsgi application
```

文件：pecan_demo/api/config.py
```
# Pecan Application Configurations
app = {
    'root': 'pecan_demo.api.root.RootController',    # 视图根节点
    'modules': ['pecan_demo.api'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/templates',
    'debug': False,
    'enable_acl': True,
    'acl_public_routes': ['/', '/v1'],
}
```

### #5 视图&路由

[Pecan 路由规则](https://pecan.readthedocs.io/en/latest/routing.html)

视图结构
```
|-- api
|   |-- __init__.py
|   |-- __init__.pyc
|   |-- app.py
|   |-- app.pyc
|   |-- config.py
|   |-- config.pyc
|   |-- hooks.py
|   |-- hooks.pyc
|   |-- middleware.py
|   |-- root.py      # RootController
|   |-- root.pyc
|   |-- run.py
|   `-- v1           # API 版本控制，便于切换  .../v1/...  or  .../v2/...
|       |-- __init__.py
|       |-- __init__.pyc
|       |-- controllers     # 业务代码
|       |   |-- __init__.py # 集成各个模块的控制器
|       |   |-- __init__.pyc
|       |   |-- demo.py     # 按功能或业务划分控制器，例如：demo
|       |   `-- demo.pyc
|       `-- datamodels      # 对应存放各模块控制器，出入参的 schema
|           `-- __init__.py

```

文件：pecan_demo/api/root.py
```
from pecan_demo.api.v1 import controllers as v1_api

class RootController(rest.RestController):
    """Root REST Controller exposing versions of the API.

    """

    v1 = v1_api.V1Controller()      # root 控制器

    @wsme_pecan.wsexpose([APIVersion])
    def index(self):
        ...
```

文件：pecan_demo/api/v1/controllers/__init__.py
```
from pecan import rest

from pecan_demo.api.v1.controllers import demo as demo_api


class V1Controller(rest.RestController):
    """API version 1 controller.

    """

    demo = demo_api.DemoController()
```

文件：pecan_demo/api/v1/controllers/demo.py
```
import pecan
from pecan import rest


class DemoController(rest.RestController):

    @pecan.expose()
    def index(self):
        return 'DemoController'
```


### #6 IDE 调试

![pycharm_conf_step1](https://images.cnblogs.com/cnblogs_com/blogs/695346/galleries/2063960/o_211117090441_pycharm_conf_step1.png "pycharm_conf_step1")

![pycharm_conf_step2](https://images.cnblogs.com/cnblogs_com/blogs/695346/galleries/2063960/o_211117090459_pycharm_conf_step2.png "pycharm_conf_step2")


![pycharm_conf_step3](https://images.cnblogs.com/cnblogs_com/blogs/695346/galleries/2063960/o_211117090518_pycharm_conf_step3.png "pycharm_conf_step3")


![test_run](https://images.cnblogs.com/cnblogs_com/blogs/695346/galleries/2063960/o_211117090536_test_run.png "test_run")



***

# 3

将前面构建的基础代码，打个包；部署到虚拟机上


## 部署

### 安装

```
# 代码
pip install pecan_demo-2021.11.2.dev6-py2.py3-none-any.whl

# 配置文件
[root@controller ~]# ll /etc/pecan_demo/
total 8
-rw-r--r-- 1 root root 123 Oct 20 10:02 api_paste.ini
-rw-r--r-- 1 root root 192 Oct 20 10:02 pecan_demo.conf

# 日志目录
[root@controller ~]# ll /var/log/pecan_demo/
total 0

```

### 建库
```
$ mysql -u root -p
MariaDB [(none)]> create database pecan_demo;
Query OK, 1 row affected (0.000 sec)

MariaDB [(none)]> grant all privileges on pecan_demo.* to 'demo'@'%' identified by '123456';
Query OK, 0 rows affected (0.275 sec)

MariaDB [(none)]> grant all privileges on pecan_demo.* to 'demo'@'controller' identified by '123456';
Query OK, 0 rows affected (0.001 sec)

MariaDB [(none)]> flush privileges;
Query OK, 0 rows affected (0.361 sec)
```


### 数据迁移
```
# 验证
[root@controller upload]# pecan-dbsync version --module pecan_demo
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
/usr/lib/python2.7/site-packages/pymysql/cursors.py:170: Warning: (1280, u"Name 'pecan_demo_alembic_pkc' ignored for PRIMARY key.")
  result = self._query(query)
[root@controller upload]#


# 生成迁移文件
[root@controller versions]# pecan-dbsync revision --autogenerate -m "init" --module pecan_demo
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'demo'
  Generating /usr/lib/python2.7/site-packages/pecan_demo/db/sqlalchemy/alembic/versions/fe92e865ca17_init.py ... done
[root@controller versions]# ll
total 8
-rw-r--r-- 1 root root 1529 Oct 20 11:57 fe92e865ca17_init.py
-rw-r--r-- 1 root root 1251 Oct 20 11:57 fe92e865ca17_init.pyc
[root@controller versions]# cat fe92e865ca17_init.py


# 迁移(执行迁移前，查看具体代码，避免删库跑路)
[root@controller versions]# pecan-dbsync upgrade --module pecan_demo
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> fe92e865ca17, init
[root@controller versions]#


# 验证
MariaDB [pecan_demo]> show tables;
+----------------------+
| Tables_in_pecan_demo |
+----------------------+
| demo                 |
| pecan_demo_alembic   |
+----------------------+
2 rows in set (0.000 sec)

MariaDB [pecan_demo]> desc demo;
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | int(11)      | NO   | PRI | NULL    | auto_increment |
| demo_id   | varchar(40)  | NO   | UNI | NULL    |                |
| desc      | text         | YES  |     | NULL    |                |
| name      | varchar(255) | NO   |     | NULL    |                |
| create_dt | datetime     | NO   |     | NULL    |                |
| update_dt | datetime     | NO   |     | NULL    |                |
| del_flag  | varchar(10)  | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
7 rows in set (0.003 sec)

MariaDB [pecan_demo]>

```

### 查看 command

```
[root@controller ~]# ll /usr/bin/ | grep pecan
-rw-r--r--    1 root root       1871 Oct 20 16:43 pecan-api
-rwxr-xr-x    1 root root        223 Oct 20 16:43 pecan-dbsync

# 调整下权限
[root@controller ~]# chmod 755 /usr/bin/pecan-api
[root@controller ~]# ll /usr/bin/ | grep pecan
-rwxr-xr-x    1 root root       1871 Oct 20 16:43 pecan-api
-rwxr-xr-x    1 root root        223 Oct 20 16:43 pecan-dbsync
```


### 启动服务

```
[root@controller ~]# pecan-api -p 8886
/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py:22: PkgResourcesDeprecationWarning: Parameters to load are deprecated.  Call .resolve and .require separately.
  return pkg_resources.EntryPoint.parse("x=" + s).load(False)
/usr/lib/python2.7/site-packages/pecan/__init__.py:122: RuntimeWarning: `static_root` is only used when `debug` is True, ignoring
  RuntimeWarning
********************************************************************************
STARTING test server pecan_demo.api.app.build_wsgi_app
Available at http://controller:8886/
DANGER! For testing only, do not use in production
********************************************************************************

```


### 请求
```
[root@controller v1]# curl -X POST \
>   http://localhost:8886/v1/demo/ \
>   -H 'Cache-Control: no-cache' \
>   -H 'Content-Type: application/json' \
>   -H 'Postman-Token: f1054175-8537-458b-82e1-bce812f42a5b' \
>   -d '{
> "name":"20211208"
> }'
{"demo_id": "5b9622aa-8deb-430a-9ab8-beb55c4519b7", "create_dt": "2021-10-21T22:52:58.643852", "name": "20211208", "update_dt": "2021-10-21T22:52:58.643852", "del_flag": null, "id": "4", "desc": null}
[root@controller v1]#
```

### 存储
```
MariaDB [pecan_demo]> select * from demo where id=4;
+----+--------------------------------------+------+----------+---------------------+---------------------+----------+
| id | demo_id                              | desc | name     | create_dt           | update_dt           | del_flag |
+----+--------------------------------------+------+----------+---------------------+---------------------+----------+
|  4 | 5b9622aa-8deb-430a-9ab8-beb55c4519b7 | NULL | 20211208 | 2021-10-21 22:52:58 | 2021-10-21 22:52:58 | 0        |
+----+--------------------------------------+------+----------+---------------------+---------------------+----------+
```



## Policy

基于 oslo_policy 进行身份or权限认证

1. enforcer.register_defaults(policies.list_rules())

    注册自定义规则

    ```
    from oslo_policy import policy

    from pecan_demo.common.policies import base

    demo_policies = [
        policy.DocumentedRuleDefault(
            name='demo:get_demo',
            check_str=base.UNPROTECTED,
            description='Return a demo.',
            operations=[{'path': '/v1/demo',
                        'method': 'GET'}]
        ),
        policy.DocumentedRuleDefault(
            name='demo:create_demo',
            check_str=base.ROLE_ADMIN,
            description='Create a new demo.',
            operations=[{'path': '/v1/demo',
                        'method': 'POST'}]
        ),
    ]
    ```

2. policy.Enforcer.authorize(action, target, context.to_dict()...)  -> rule, target, creds

    将待校验参数,传入认证接口

    ```
    context   -> pecan.request.context
    action    -> 'demo:create_demo'
    target    -> {} or {"tenant_id": <tenant_uuid>}

    oslo_policy.policy.Enforcer#authorize
      ->
      return self.enforce(rule, target, creds, do_raise, exc, *args, **kwargs)
    ```



loading








