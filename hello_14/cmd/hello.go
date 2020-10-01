package main

import (
	"flag"
	"os"
	// "regexp"
	"time"

	"github.com/sirupsen/logrus"
	"hello_14/db"
)

var log = logrus.New()

func init() {
	Formatter := new(logrus.TextFormatter)
	Formatter.TimestampFormat = "02-01-2006 15:04:05"
	Formatter.FullTimestamp = true
	logrus.SetFormatter(Formatter)

	log.Out = os.Stdout
	/*
		file, err := os.OpenFile("./log/finance.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
		if err == nil {
			logrus.SetOutput(file)
		} else {
			log.Info("Failed to log to file, using default stderr")
		}
	*/
}

func main() {
	plat := flag.String("plat", "cp", "来源平台名称")
	//区分全量增量，不带此选项默认是增量处理
	inc := flag.Bool("inc", false, "全量增量标志")
	addon := flag.Bool("addon", false, "增量回补标志")
	table := flag.String("table", "default", "数据表名称")
	//暂定mmdd格式
	date := flag.String("date", "20180101", "交易日期8位")

	var addon_flag string

	flag.Parse()

	if *inc {
		_, err := time.Parse("20060102", *date)
		if err != nil {
			log.Fatal(err)
		}

		d := *date

		if *addon {
			addon_flag = "1"
		} else {
			addon_flag = "0"
		}

		//处理增量数据
		act, ok := db.IncTableMappingAction[*table]
		if ok == true {
			act(*plat, *table, 4, d, addon_flag)
		} else {
			log.Info("no table name")
		}

	} else {
		//处理全量数据
	}
}
