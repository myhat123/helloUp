godror
======

https://github.com/godror/godror

godror is a package which is a database/sql/driver.Driver for connecting to Oracle DB, using Anthony Tuininga's excellent OCI wrapper, ODPI-C.

At least Go 1.13 is required! Cgo is required, so cross-compilation is hard, and you cannot set CGO_ENABLED=0!

Although Oracle Client libraries are NOT required for compiling, they are needed at run time. Download the free Basic or Basic Light package from https://www.oracle.com/database/technologies/instant-client/downloads.html.

ODPI-C 集成在包内  
要求Go 1.13以上，Cgo是需要开放选项的  
Oracle instantclient需要安装

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

oracle
======
sudo apt install libaio1

oracle instantclient
ORACLE_HOME下

ln -s libclntsh.so.12.1 libclntsh.so

构建
====

go build -mod=vendor cmd/hello.go 

运行
====

./hello --inc --table sav_qry_cdm_dtl --date 20200915