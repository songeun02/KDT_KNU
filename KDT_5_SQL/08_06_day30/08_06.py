import pymysql
import pandas as pd
import csv

import pymysql.cursors

# conn=pymysql.connect(host='localhost', user='root',password='1216',db='sakila',charset='utf8')

# cur=conn.cursor()
# cur.execute('select * from language')

# desc=cur.description # 헤더 정보 가져옴
# for i in range(len(desc)):
#     print(desc[i][0], end=' ')
# print()

# rows=cur.fetchall() # 모든 데이터 가져옴 
# for data in rows:
#     print(data)
# print()

# language_df=pd.DataFrame(rows)
# print(language_df)

# cur.close()
# conn.close() # db 연결 종료

# print('df')

# print(language_df)

# -----------------------------------------------------------

# conn=pymysql.connect(host='localhost', user='root',password='1216',db='sakila',charset='utf8')

# cur=conn.cursor(pymysql.cursors.DictCursor)
# cur.execute('select * from language')
# rows=cur.fetchall()

# language_df=pd.DataFrame(rows)
# print(language_df)

# print()
# print(language_df['name'])
# cur.close()
# conn.close()


# print(language_df)

# -----------------------------------------------------------

# conn=pymysql.connect(host='localhost', user='root',password='1216',db='sakila',charset='utf8')

# cur=conn.cursor()

# query = """
# select c.email from customer as c
# inner join rental as r
# on c.customer_id = r.customer_id
# where date(r.rental_date) = (%s)"""

# cur.execute(query, ('2005-06-14'))
# rows = cur.fetchall()
# for row in rows:
#     print(row)

# cur.close()
# conn.close()

# ---------------------------------------------------------------------

def create_table(conn, cur):
    try:
        query1 = "drop table if exists customer_m"
        query2 = """ 
                create table customer_m
                (name varchar(10), 
                category smallint,
                region varchar(10))
                """
        cur.execute(query1)
        cur.execute(query2)
        conn.commit()
        print('Table 생성 완료')
    except Exception as e:
        print(e)

def main():
    conn=pymysql.connect(host='localhost', user='root',password='1216',db='sqlclass_db',charset='utf8')
    cur=conn.cursor()

    create_table(conn,cur)

    cur.close()
    conn.close()
    print('DataBase 연결 종료')



# ----------------------------------------------------------------------

# conn=pymysql.connect(host='localhost', user='root',password='1216',db='sqlclass_db',charset='utf8')

# curs=conn.cursor()
# sql = """insert into customer_m(name, category, region) 
# values (%s, %s, %s)"""

# curs.execute(sql, ('홍길동',1,'서울'))
# curs.execute(sql, ('이연수',2,'서울'))
# conn.commit()

# print('insert 완료')

# curs.execute('select * from customer')
# rows=curs.fetchall()
# print(rows)

# curs.close()
# conn.close()

# -----------------------------------------------------------------

# conn=pymysql.connect(host='localhost', user='root',password='1216',db='sqlclass_db',charset='utf8')
# curs=conn.cursor()

# sql="""insert into customer_m(name, category, region)
# values (%s, %s, %s)"""

# data=(('홍진우',1,'서울'),('강지수',2,'부산'),('김청진',1,'대구'))

# curs.executemany(sql, data)

# conn.commit()
# print('executemany() 완료')
# curs.close()
# conn.close()

# --------------------------------------------------------------

conn=pymysql.connect(host='localhost', user='root',password='1216',db='sqlclass_db',charset='utf8')

curs=conn.cursor()

sql="""update customer_m 
set region = '서울특별시' where region='서울'"""

curs.execute(sql)

print('update 완료')

sql = "delete from customer_m where name =%s"
curs.execute(sql, '홍길동')
print('delete 홍길동')

conn.commit()
conn.close()