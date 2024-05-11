# 주가 크롤링
# 퀀트 투자를 위한 백테스트나 종목선정을 위해서는 수정주가가 필

 
from sqlalchemy import create_engine
import pandas as pd

#engine = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/stock_db')
query="""
select * from kor_ticker
where 기준일 =(select max(기준일) from kor_ticker)
and 종목구분 = '보통주';
"""

#ticker_list = pd.read_sql(query, con=engine)
#engine.dispose()

import pymysql

# 데이터베이스 연결 설정
conn = pymysql.connect(host='127.0.0.1', user='root', password='a1536613', db='stock_db', charset='utf8')

try:
    # Cursor 객체 생성
    with conn.cursor() as cursor:
        # SQL 쿼리 실행
        cursor.execute("SELECT * FROM kor_ticker")
        
        # 결과 모두 가져오기
        results = cursor.fetchall()
        
        # 결과 출력
        for row in results:
            print(row)

finally:
    # 데이터베이스 연결 종료
    conn.close()
