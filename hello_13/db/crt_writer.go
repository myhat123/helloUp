package db

import (
	// "strings"
	"time"

	_ "github.com/mattn/go-oci8"
	log "github.com/sirupsen/logrus"
	"gopkg.in/inf.v0"

	"hello_13/tasks"
)

/*
	Author: dzy
	h03 活期交易明细表
	参数说明:
		plat:  平台来源
		table: 表名
		size:  分批导入阀门值，以百万条记录数为单位
		date:  可变参数，增量日期|回补标志
*/
func GetQryCdmDtl(plat string, table string, size int, date ...string) {
	session := connectSession()
	start := time.Now()

	db, table_name := getDbTable(plat, table, date...)
	defer db.Close()

	startLog(table, date...)

	rows, err := db.Query(`
		select acc, tran_date, sys_seqno, dtl_seqno,
		       tran_inst, bal, amt, amt_type, tran_code,
		       csh_tsf_flag, dr_cr_flag, accu, rpt_sum,
		       n_tran_type, timestamp1, opr_tlr, b_sub_tab_flag, bgn_int_date 
		from ` + table_name + ` where rownum<=1000`)

	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	//金融下载平台处理日期型是从18991231开始计算
	//采用UTC是为了写入cassandra时日期不错位
	cpstart := time.Date(1899, 12, 31, 0, 0, 0, 0, time.UTC)

	records := make([]*tasks.CQryCdmDtl, 0)
	i := 0
	for rows.Next() {
		d := new(DQryCdmDtl)
		t := new(tasks.CQryCdmDtl)

		err := rows.Scan(
			&d.Acc, &d.TranDate, &d.SysSeqno, &d.DtlSeqno,
			&d.TranInst, &d.Bal, &d.Amt,
			&d.AmtType, &d.TranCode, &d.CshTsfFlag,
			&d.DrCrFlag, &d.Accu, &d.RptSum, &d.NTranType, &d.Timestamp1,
			&d.OprTlr, &d.BSubTabFlag, &d.BgnIntDate)
		if err != nil {
			log.Fatal(err)
		}

		if d.Acc.Valid && d.SysSeqno.Valid {
			if i > 0 && i%(size*100*10000) == 0 {
				tasks.InitChan()
				tasks.Start(session, records)
				records = make([]*tasks.CQryCdmDtl, 0)

				processLog(table, start, i, date...)
			}

			t.Acc = d.Acc.String
			t.TranDate = cpstart.AddDate(0, 0, int(d.TranDate.Int64))
			t.SysSeqno = d.SysSeqno.String
			t.DtlSeqno = d.DtlSeqno
			t.TranInst = d.TranInst.String

			y := new(inf.Dec)
			y.SetString(d.Bal)
			t.Bal = y

			k := new(inf.Dec)
			k.SetString(d.Amt)
			t.Amt = k

			t.AmtType = d.AmtType
			t.TranCode = d.TranCode.String
			t.CshTsfFlag = d.CshTsfFlag
			t.DrCrFlag = d.DrCrFlag
			t.TranInst = d.TranInst.String

			l := new(inf.Dec)
			l.SetString(d.Accu)
			t.Accu = l

			t.RptSum = d.RptSum.String
			t.NTranType = d.NTranType
			t.Timestamp1 = d.Timestamp1.String
			t.OprTlr = d.OprTlr.String
			t.BSubTabFlag = d.BSubTabFlag
			t.BgnIntDate = cpstart.AddDate(0, 0, int(d.BgnIntDate.Int64))

			records = append(records, t)
			i = i + 1
		}
	}

	if err = rows.Err(); err != nil {
		log.Fatal(err)
	}

	tasks.InitChan()
	tasks.Start(session, records)

	//写入日志最新状态
	// msg := collectMsg(table, start, time.Now(), i, date...)
	// writeLog(msg)

	endLog(table, start, i, date...)
}