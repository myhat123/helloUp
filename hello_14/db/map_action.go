package db

//对应一系列writer导入数据的函数
type Action func(string, string, int, ...string)

var IncTableMappingAction = map[string]Action{
	//h3 活期交易明细表插入 dzy
	"sav_qry_cdm_dtl": GetQryCdmDtl,
}
