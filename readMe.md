## 环境搭建

### Docker
```shell
# apt包列表完全更新
apt-get update -y
# 安装Get
apt install git
# 安裝Docker
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
service docker start

# 开机自启
sudo systemctl enable docker
```

### Python
```shell
docker run -itd --name=Backend -p 80:80 -v /home/0xFloor_backend:/home python:3.9.0 bash

docker exec -it Backend /bin/bash
cd /home/

lsof -i:8000
python manage.py runserver 0.0.0.0:8000

apt-get update -y
apt-get install vim
```

### python 依赖
```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple Django==3.2.18
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django-rest-auth==0.9.5
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django-allauth==0.40.0
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django-filter==2.4.0
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple cryptography
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple drf-yasg
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple python3-openid
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pymysql
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple tronpy
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple loguru
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django-crontab
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django-cors-headers
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django-filter
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple django-simpleui

```

### 数据库
```shell
docker run \
--restart=always -d \
--name mysql \
-p 3306:3306 \
-v /home/mysql/conf.d/:/etc/mysql/conf.d \
-v /home/mysql/mysql/:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=123456 \
mysql
  
docker exec -it mysql /bin/bash

mysql -hlocalhost -uroot -p123456

use mysql;
update user set host = '%' where user = 'root';
FLUSH PRIVILEGES

# 两个docker 建立连接
docker network create -d bridge network1
docker network connect network1 mysql
docker network connect network1 Backend
docker network connect network1 Khala

# 看IP
```

### 创建超级管理员
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 报错
1. pymysql报错：cryptography is required for sha256_password or caching_sha2_password
```shell
# 其实 cryptography 是一个python包，所以解决方法很简单
pip install cryptography
```

1. ImportError: cannot import name 'FieldDoesNotExist' from 'django.db.models' 
```shell
vi /usr/local/lib/python3.9/site-packages/allauth/utils.py

# from django.db.models import FieldDoesNotExist, FileField
# 换成
# from django.core.exceptions import FieldDoesNotExist
```

```shell
lsof -i:80
python manage.py runserver 0.0.0.0:80
```

### 定时任务启动
```shell
apt-get update
apt-get install cron
service cron start
service cron status

python manage.py crontab remove
python manage.py crontab add
```