下载这些包的位置存放
=================

```sh
export GOBIN=~/go/bin
```

放在 ~/go/pkg/mod 中

依赖包
=====
复制mod至vendor中

go mod vendor

go-oci8
=======

oci8.pc文件

prefix=/usr
includedir=${prefix}/local/instantclient_12_2/sdk/include
libdir=${prefix}/local/instantclient_12_2

Name: oci8
Description: Oracle Instant Client
Version: 12.2
Cflags: -I${includedir}
Libs: -L${libdir} -lclntsh

环境变量
=======
export PKG_CONFIG_PATH=/home/hzg/work/helloGo/hello_13/vendor/github.com/mattn/go-oci8
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/instantclient_12_2

安装pkg-config

sudo apt install pkg-config

oracle
======
oracle instantclient
ORACLE_HOME下

ln -s libclntsh.so.12.1 libclntsh.so

构建
====
sudo apt install libaio1

go build -mod=vendor cmd/hello.go 

运行
====

./hello --inc --table sav_qry_cdm_dtl --date 20200915