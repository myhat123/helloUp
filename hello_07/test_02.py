from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from datetime import date
from decimal import Decimal
from typing import Dict, List

def get_data(filename: str) -> List[str]:
    data = []
    f = open(filename, 'rt')
    for r in f.readlines()[2:-1]:
        x = r.strip('\n').split(',')
        # data.append([y.strip() for y in x])
        y = [date.fromisoformat(x[0]), x[1], x[2], Decimal(x[3]), int(x[4]), x[5]]
        data.append(y)

    f.close()

    return data

class CassDB:

    def __init__(self):
        auth_provider = PlainTextAuthProvider(
            username="cassandra",
            password="cassandra"
        )

        self.cluster = Cluster(['localhost'], auth_provider=auth_provider)
        self.session = self.cluster.connect('finance')

    def close(self):
        self.cluster.shutdown()

    def write_data(self, data: str):
        for x in data:
            self.session.execute("""
                insert into finance.brch_qry_dtl (
                    tran_date, timestamp1, acc, 
                    amt, dr_cr_flag, rpt_sum) 
                    values (
                        %s, %s, %s, 
                        %s, %s, %s)
            """, (
                x[0], x[1], x[2], 
                x[3], x[4], x[5]
            ))

if __name__  == '__main__':
    d = get_data('../data-files/data.csv') 
    #print(d)
    c = CassDB()
    c.write_data(d)
    c.close()
