create table finance.brch_qry_dtl (
    acc character varying(19), 
    tran_date date, 
    amt numeric(16,2), 
    dr_cr_flag integer, 
    rpt_sum character varying(8), 
    timestamp1 character varying(14)
);

create index brch_qry_dtl_acc_index on brch_qry_dtl (tran_date, acc);