use finance;

//h03
CREATE TABLE qry_cdm_dtl (
  acc text,
  tran_date date,
  sys_seqno text,
  dtl_seqno int,
  tran_inst text,
  bal decimal,
  amt decimal,
  amt_type int,
  tran_code text,
  csh_tsf_flag int,
  dr_cr_flag int,
  accu decimal,
  rpt_sum text,
  n_tran_type int,
  timestamp1 text,
  opr_tlr text,
  b_sub_tab_flag int,
  bgn_int_date date,
  PRIMARY KEY (acc, tran_date, sys_seqno, dtl_seqno, timestamp1)
);