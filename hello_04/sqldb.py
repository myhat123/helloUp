import psycopg2
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, List

#原始数据库表
#CONN_STR = 'postgresql://jxyz:1234@localhost/jr'

#pgbouncer连接字符串
CONN_STR = 'postgresql://jxyz:1234@localhost:6432/db_jr'

class SQLDB(object):
    def __init__(self, conn):
        self.conn = psycopg2.connect(conn)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()


    def write_data(self, data: str):
        for x in data:
            self.cursor.execute("""
                insert into finance.brch_qry_dtl (
                    tran_date, timestamp1, acc, 
                    amt, dr_cr_flag, rpt_sum) 
                    values (
                        %s, %s, %s, 
                        %s, %s, %s)
            """, (
                x[0], x[1], x[2], 
                Decimal(x[3]), int(x[4]), x[5]
            ))

        self.conn.commit()

    def read_data(self):
        self.cursor.itersize = 20000

        self.cursor.execute("""
            select acc, tran_date, rpt_sum, dr_cr_flag, amt FROM brch_qry_dtl
        """)

        results = []
        for r in self.cursor.fetchall():
            d = dict()
            d['acc'] = r[0]
            d['tran_date'] = r[1]
            d['rpt_sum'] = r[2]
            d['dr_cr_flag'] = r[3]
            d['amt'] = r[4]

            results.append(d)

        return results

def get_data(filename: str) -> List[str]:
    data = []
    f = open(filename, 'rt')
    for r in f.readlines()[2:-1]:
        x = r.strip('\n').split('|')
        data.append([y.strip() for y in x])

    f.close()

    return data

def load_data():

    d = get_data('../data-files/data.csv')
    sdb = SQLDB(CONN_STR)
    results = []
    for r in d:
        x = r[0].split(',')
        results.append([x[0], x[1], x[2], x[3], x[4], x[5]])

    sdb.write_data(results)

if __name__ == '__main__':
    load_data()