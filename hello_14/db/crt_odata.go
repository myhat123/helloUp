package db

import (
	"database/sql"
)

/*
	Author: dzy
	h03 活期交易明细表
*/
type DQryCdmDtl struct {
	Acc         sql.NullString
	TranDate    sql.NullInt64
	SysSeqno    sql.NullString
	DtlSeqno    int
	TranInst    sql.NullString
	Bal         string
	Amt         string
	AmtType     int
	TranCode    sql.NullString
	CshTsfFlag  int
	DrCrFlag    int
	Accu        string
	RptSum      sql.NullString
	NTranType   int
	Timestamp1  sql.NullString
	OprTlr      sql.NullString
	BSubTabFlag int
	BgnIntDate  sql.NullInt64
}