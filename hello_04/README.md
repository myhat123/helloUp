postgresql
==========

参考资料

https://wiki.postgresql.org/wiki/Apt

1. 导入 the repository key from https://www.postgresql.org/media/keys/ACCC4CF8.asc

```sh
sudo apt-get install curl ca-certificates gnupg
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```
2. 创建 /etc/apt/sources.list.d/pgdg.list

ubuntu 18.04, 加入如下

```sh
deb http://apt.postgresql.org/pub/repos/apt bionic-pgdg main
```

或者

```sh
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```

3. 安装postgresql-12

```sh
sudo apt-get update
sudo apt-get install postgresql-12
```