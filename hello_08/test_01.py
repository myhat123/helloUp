import pandas as pd

import psycopg2

CONN_STR = 'postgresql://jxyz:1234@localhost:6432/db_jr'
conn = psycopg2.connect(CONN_STR)

df = pd.read_sql('''
    select acc, rpt_sum, amt from finance.brch_qry_dtl
''', conn)

print(df)