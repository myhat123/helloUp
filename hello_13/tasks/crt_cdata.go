package tasks

import (
	"time"

	"gopkg.in/inf.v0"
)

/*
	Author: dzy
	h03 活期交易明细表
*/
type CQryCdmDtl struct {
	Acc         string
	TranDate    time.Time
	SysSeqno    string
	DtlSeqno    int
	TranInst    string
	Bal         *inf.Dec
	Amt         *inf.Dec
	AmtType     int
	TranCode    string
	CshTsfFlag  int
	DrCrFlag    int
	Accu        *inf.Dec
	RptSum      string
	NTranType   int
	Timestamp1  string
	OprTlr      string
	BSubTabFlag int
	BgnIntDate  time.Time
}