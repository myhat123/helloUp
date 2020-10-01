package db

import (
	"database/sql"
	// "fmt"
	"time"

	"github.com/gocql/gocql"
	log "github.com/sirupsen/logrus"
)

var PREFETCH_COUNT = 20000
var ARRAY_SIZE = 20000

//连接cassandra集群
func connectSession() *gocql.Session {
	cluster := gocql.NewCluster("localhost")
	cluster.Keyspace = "finance"
	cluster.Consistency = gocql.Quorum
	cluster.Timeout = 1 * time.Minute
	cluster.ProtoVersion = 4
	cluster.PageSize = 20000
	cluster.PoolConfig.HostSelectionPolicy = gocql.TokenAwareHostPolicy(gocql.RoundRobinHostPolicy())

	cluster.Authenticator = gocql.PasswordAuthenticator{
		Username: "cassandra",
		Password: "cassandra",
	}

	session, _ := cluster.CreateSession()
	time.Sleep(1 * time.Second)

	return session
}

//金融下载平台连接字符串
func getCPDSN() string {
	s := "test/test@cpdata"
	return s
}

//共享平台连接字符串
func getGXDSN() string {
	s := "petl/test@ycldb"
	return s
}

//获取下载平台的增量表名用户
func getCPIncDBUser() string {
	return "cpdds_sdata"
}

//获取下载平台的全量表名用户
func getCPAllDBUser() string {
	return "cpdds_pdata"
}

//获取共享平台的增量表名用户
func getGXIncDBUser() string {
	return "ycladd"
}

//获取共享平台的全量表名用户
func getGXAllDBUser() string {
	return "ycltotal"
}

func getDbTable(plat string, table string, date ...string) (d *sql.DB, t string) {

	var table_name string
	var db *sql.DB

	if plat == "cp" {
		db, _ = sql.Open("godror", getCPDSN())
		table_name = getCPTableName(table, date...)
	} else if plat == "gx" {
		db, _ = sql.Open("godror", getGXDSN())
		table_name = getGXTableName(table, date...)
	}

	return db, table_name
}

func getGXTableName(t string, d ...string) string {
	var table string

	if d != nil {
		table = getGXIncDBUser() + "." + t + "_" + d[0][4:8]
	} else {
		table = getGXAllDBUser() + "." + t
	}
	return table
}

func getCPTableName(t string, d ...string) string {
	var table string

	if d != nil {
		table = getCPIncDBUser() + "." + t + "_" + d[0][4:8]
	} else {
		table = getCPAllDBUser() + "." + t
	}
	return table
}

func startLog(t string, d ...string) {
	if d != nil {
		log.WithFields(log.Fields{
			"table": t,
			"date":  d[0],
		}).Info("Start fetching DB...")
	} else {
		log.WithFields(log.Fields{
			"table": t,
		}).Info("Start fetching DB...")
	}
}

func processLog(t string, start time.Time, i int, d ...string) {
	if d != nil {
		log.WithFields(log.Fields{
			"table":   t,
			"date":    d[0],
			"time":    time.Now().Sub(start).Seconds(),
			"records": i,
		}).Info("Processing is")
	} else {
		log.WithFields(log.Fields{
			"table":   t,
			"time":    time.Now().Sub(start).Seconds(),
			"records": i,
		}).Info("Processing is")
	}
}

func endLog(t string, start time.Time, i int, d ...string) {
	if d != nil {
		log.WithFields(log.Fields{
			"table":   t,
			"date":    d[0],
			"time":    time.Now().Sub(start).Seconds(),
			"records": i,
		}).Info("Finish import cass")
	} else {
		log.WithFields(log.Fields{
			"table":   t,
			"time":    time.Now().Sub(start).Seconds(),
			"records": i,
		}).Info("Finish import cass")
	}

}
