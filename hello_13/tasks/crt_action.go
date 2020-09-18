package tasks

import (
	log "github.com/sirupsen/logrus"

	"github.com/gocql/gocql"
	"github.com/scylladb/gocqlx"
	"github.com/scylladb/gocqlx/qb"
)

/*
	Author: dzy
	h03 活期交易明细表
*/
func insQryCdmDtl(session *gocql.Session, records []*CQryCdmDtl) {
	for _, t := range records {
		
		// if err := session.Query(`
		// 		INSERT INTO qry_cdm_dtl (
		// 			acc, tran_date, sys_seqno, dtl_seqno, tran_inst, bal, amt,
		// 			amt_type, tran_code, csh_tsf_flag, dr_cr_flag, accu, rpt_sum, n_tran_type, timestamp1,
		// 			opr_tlr, b_sub_tab_flag, bgn_int_date)
		// 		VALUES (
		// 			?, ?, ?, ?, ?, ?, ?,
		// 			?, ?, ?, ?, ?, ?, ?, ?,
		// 			?, ?, ?
		// 		)`, t.Acc, t.TranDate, t.SysSeqno, t.DtlSeqno, t.TranInst, t.Bal, t.Amt,
		// 	t.AmtType, t.TranCode, t.CshTsfFlag, t.DrCrFlag, t.Accu, t.RptSum, t.NTranType, t.TimeStamp1,
		// 	t.OprTlr, t.BSubTabFlag, t.BgnIntDate).Exec(); err != nil {
		// 	log.Fatal(err)
		// }
		

		stmt, names := qb.Insert("qry_cdm_dtl").
			Columns("acc", "tran_date", "sys_seqno", "dtl_seqno", "tran_inst", "bal", "amt",
				"amt_type", "tran_code", "csh_tsf_flag", "dr_cr_flag", "accu", "rpt_sum", "n_tran_type", "timestamp1",
				"opr_tlr", "b_sub_tab_flag", "bgn_int_date").
			ToCql()

		q := gocqlx.Query(session.Query(stmt), names)
		defer q.Release()

		if err := q.BindStruct(t).Exec(); err != nil {
			log.Fatal(err)
		}
	}
}