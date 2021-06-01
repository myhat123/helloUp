pyenv
=====

python多版本管理

主要是解决python 3.x，ubuntu 18.04 老版本仍默认安装python2

构建包安装
=========

两个文档，不知道哪个为准了？

https://github.com/pyenv/pyenv/wiki/Common-build-problems

sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

https://github.com/pyenv/pyenv/wiki

sudo apt-get install --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

自动安装
=======

比较简单的方式

The automatic installer  
https://github.com/pyenv/pyenv-installer

curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

直接下载 pyenv-installer 脚本

chmod +x pyenv-installer
./pyenv-installer

配置.bashrc

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

安装python
==========

查看能安装的python各类版本  
pyenv install --list

查看已经安装的python各版本  
pyenv versions

构建单独的虚拟环境  
pyenv virtualenv 3.8.6 gopy3
pyenv activate gopy3

配置~/.pip/pip.conf
==================

```ini
[global]
index-url = https://mirrors.cloud.tencent.com/pypi/simple
[install]
trusted-host = mirrors.cloud.tencent.com
```

升级pip
======
/home/hzgtest/.pyenv/versions/3.8.6/envs/gopy3/bin/python3.8 -m pip install --upgrade pip

supervisor
==========

后台服务脚本

supervisor 4.0以上版本，开始支持python 3.4及以上版本

ubuntu 18.04仍然是supervisor 3.x版本

fabric
======

远程部署工具

2 to 3
======

https://six.readthedocs.io/

Six: Python 2 and 3 Compatibility Library

可以参考Six库，其中有2和3的对比

字符集统一使用unicode

>>> x = 'abc'
>>> x.encode()
b'abc'
>>> x.encode().decode()
'abc'

项目使用了 cryptography

pip install cryptography

加解密的过程，涉及到编码转换

校验码生成图片, 使用了pillow  
pip install pillow

StringIO -> BytesIO