import pandas as pd

import psycopg2

from datetime import datetime

CONN_STR = 'postgresql://jxyz:1234@localhost:6432/db_jr'

def conv_time(t):
    return datetime.strptime(t, '%Y%m%d%H%M%S')

class QryRec:
    def __init__(self):
        self.conn = psycopg2.connect(CONN_STR)
 
    def get_qry_dtl(self, d):
        self.df = pd.read_sql('''
            select acc, rpt_sum, amt, dr_cr_flag, timestamp1 
            from finance.brch_qry_dtl
            where tran_date=%s
        ''', self.conn, params=(d,))

    def total_amt(self, dr_cr_flag=1):
        # select sum(amt) from brch_qry_dtl where dr_cf_flag=%s
        return self.df[self.df['dr_cr_flag']==dr_cr_flag]['amt'].sum()

    def total_amt_apart(self, dr_cr_flag=1):
        # 之前已经过滤了日期
        # select rpt_sum, sum(amt) from brch_qry_dtl where dr_cr_flag=%s
        x = self.df
        rows = x[x['dr_cr_flag']==dr_cr_flag].groupby('rpt_sum').agg({'amt': 'sum'})

        rec = []
        for r in rows.itertuples():
            d = dict()
            d['rpt_sum'] = r[0]
            d['amt'] = r[1]

            rec.append(d)

        return rec

    def get_acc_detail(self, dr_cr_flag, rpt_sum):

        # select * from brch_qry_dtl where dr_cr_flag=%s and rpt_sum=%s
        x = self.df
        rows = x[(x['dr_cr_flag']==dr_cr_flag) & (x['rpt_sum'] == rpt_sum)]

        rec = []
        for r in rows.itertuples():
            d = dict()
            d['acc'] = r.acc
            d['amt'] = r.amt
            d['timestamp1'] = r.timestamp1

            rec.append(d)

        return rec

    def total_every_30min(self):

        #转换，增加一列time
        self.df['time'] = self.df['timestamp1'].map(conv_time)

        #排序，不改变原有的dataframe
        x = self.df.sort_values(by=['time'], ascending=True)
        y = x[['amt', 'time']].resample('30min', on='time').sum()

        rec = []
        for r in y.itertuples():
            d = dict()

            #time作为Index
            d['time'] = r.Index
            d['amt'] = r.amt

            rec.append(d)

        return rec

    def total_every_30min_cumsum(self):

        #转换，增加一列time
        self.df['time'] = self.df['timestamp1'].map(conv_time)

        #排序，不改变原有的dataframe
        x = self.df.sort_values(by=['time'], ascending=True)
        y = x[['amt', 'time']].resample('30min', on='time').sum().cumsum()

        #转换Index为Column
        y.reset_index(inplace=True)
        y = y.rename(columns={'index': 'time'})
        
        rec = []
        for r in y.itertuples():
            d = dict()

            #time作为Column
            d['time'] = r.time
            d['amt'] = r.amt

            rec.append(d)

        return rec

if __name__ == '__main__':
    q = QryRec()
    q.get_qry_dtl('2019-11-27')
    # print(q.total_amt_apart())
    # print(q.get_acc_detail(1, '他行来账'))
    print(q.total_every_30min_cumsum())