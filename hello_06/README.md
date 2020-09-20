airflow
=======

参考资料:  
http://airflow.apache.org/docs/stable/start.html

```sh
# airflow needs a home, ~/airflow is the default,
# but you can lay foundation somewhere else if you prefer
# (optional)
export AIRFLOW_HOME=~/airflow

# install from pypi using pip
pip install 'apache-airflow[postgres]'

# initialize the database
airflow initdb

# start the web server, default port is 8080
airflow webserver -p 8080

# start the scheduler
airflow scheduler
```

postgresql
==========

sudo su
su - postgres
createuser -P -e test (密码: 1234)
createdb -O test -E utf8 airflow

postgresql://test:1234@localhost/airflow

airflow.cfg
===========

参考资料:  
https://airflow.readthedocs.io/en/stable/howto/initialize-database.html
https://www.cnblogs.com/braveym/category/1530800.html

executor = LocalExecutor
sql_alchemy_conn = postgresql://test:1234@localhost/airflow

# 这个配置只有在第一次启动airflow之前设置才有效
load_examples = False

# 修改检测新dag间隔
min_file_process_interval = 10

# scheduler 将并行生成多个线程来调度 dags
max_threads = 2

parallelism = 32
dag_concurrency = 16
max_active_runs_per_dag = 16

# 时区
default_timezone = Asia/Shanghai
default_ui_timezone = Asia/Shanghai


重置db
airflow resetdb

Airflow添加用户登录
=================

https://airflow.apache.org/docs/stable/security.html#web-authentication
https://www.cnblogs.com/braveym/p/12661735.html

https://stackoverflow.com/questions/52056809/how-to-activate-authentication-in-apache-airflow  
https://www.cloudwalker.io/2020/03/01/airflow-rbac-role-based-access-control/#:%7E:text=RBAC%20is%20the%20quickest%20way,access%20to%20DAGs%20as%20well

在 airflow.cfg 文件中 [webserver] 下添加如下配置

[webserver]
authenticate = True
auth_backend = airflow.contrib.auth.backends.password_auth
rbac = True

airflow create_user -r Admin -u admin -f hu -l zg -p 1234 -e myhat123@gmail.com

airflow resetdb

增加了用户权限后，web ui的界面完全不一样了，时区也显示正常了

gunicorn进程
============

airflow webserver 不断有ttin, ttou, 与配置有关

https://stackoverflow.com/questions/47868787/handling-signal-ttou-message-while-running-dag-in-airflow

Those messages are expected. The ttou (and ttin) signals are used to refresh gunicorn workers of the webserver so that it picks up DAG changes. You can modify or disable this behavior with the worker_refresh_interval and worker_refresh_batch_size airflow config values.

# Number of workers to refresh at a time. When set to 0, worker refresh is
# disabled. When nonzero, airflow periodically refreshes webserver workers by
# bringing up new ones and killing old ones.

# 修改为0，不再检测DAG的变化
worker_refresh_batch_size = 0

airflow tutorial
================

示例代码:  
https://airflow.apache.org/docs/stable/tutorial.html#

template command 采用了jinja模板
{{ ds }}
{{ macros }}  
    airflow.macros.ds_add(ds, days)
{{ params }}

设置依赖关系
t1 >> [t2, t3]
t1.set_downstream([t2, t3])

t2, t3 依赖于 t1, t1先执行，然后执行t2, t3

cp tutorial.py ~/airflow/dags

dag运行间隔周期
=============

https://airflow.apache.org/docs/stable/dag-run.html

Crontab guru  https://crontab.guru/

格式: (minute hour (month day) month (week day))

删除dag  
airflow delete_dag tutorial

dag的调度时间
============

```python
from datetime import datetime, timedelta

def days_ago(n, hour=0, minute=0, second=0, microsecond=0):
    today = datetime.now().replace(
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond)
    
    return today - timedelta(days=n)
```

覆盖 

from airflow.utils.dates import days_ago

airflow中的days_ago，使用的是 timezone.utcnow()  
那我们需要转到本地的时区，需要直接使用 datetime.now()

这样处理之后，如下的调度间隔周期是按照正常的本地时间来走的

schedule_interval='0 10 * * *'