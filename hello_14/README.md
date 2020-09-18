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