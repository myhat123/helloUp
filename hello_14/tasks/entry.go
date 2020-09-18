package tasks

import (
	"github.com/gocql/gocql"
)

//写入数据至cassandra
func writeCassDB(session *gocql.Session, data interface{}) bool {

	//h03 活期交易明细表插入 dzy
	if savqrys, ok := data.([]*CQryCdmDtl); ok {
		insQryCdmDtl(session, savqrys)
	}
	
	return true
}
