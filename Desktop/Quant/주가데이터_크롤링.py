# 주가 크롤링
# 퀀트 투자를 위한 백테스트나 종목선정을 위해서는 수정주가가 필

 
from sqlalchemy import create_engine
import pandas as pd
import pymysql
from dateutil.relativedelta import relativedelta
import requests as rq
from io import BytesIO
from datetime import date
import time
from tqdm import tqdm
import re

engine = create_engine('mysql+pymysql://root:a1536613@127.0.0.1:3306/stock_db')
query="""
select * from kor_ticker
where 기준일 =(select max(기준일) from kor_ticker)
and 종목구분 = '보통주';
"""

ticker_list = pd.read_sql(query, con=engine)
engine.dispose()

'''
i = 0
ticker = ticker_list['종목코드'][i]
# 5년전 정보부터 수집
fr = ((date.today()) + relativedelta(years=-5)).strftime("%Y%m%d")
to = (date.today()).strftime("%Y%m%d")


url = f'''https://fchart.stock.naver.com/siseJson.nhn?symbol={ticker}&requestType=1&startTime={fr}&endTime={to}&timeframe=day'''

data = rq.get(url).content
data_price = pd.read_csv(BytesIO(data))


# 일부 필요없는 칼럼 제외
price = data_price.iloc[:, 0:6] 
price.columns = ['날짜', '시가', '고가','저가','종가','거래량']
price = price.dropna()

price['날짜'] = price['날짜'].str.extract('(\d+)')
price['날짜'] = pd.to_datetime(price['날짜'])
price['종목코드'] = ticker




# DB에 넣어주기
conn = pymysql.connect(host='127.0.0.1', 
                       user='root', 
                       password='a1536613',
                       db='stock_db',
                       charset='utf8')
'''

'''
try:
    # 커서 생성
    with conn.cursor() as cursor:
        # SQL 실행
        cursor.execute("USE stock_db;")
        cursor.execute("""
            CREATE TABLE kor_price (
                날짜 DATE,
                시가 double,
               고가 double,
               저가 double,
               종가 double,
               거래량 double,
               종목코드 varchar(6),
               primary key(날짜, 종목코드)
            );
        """)
        

        conn.commit()

finally:
    # 데이터베이스 연결 종료
    conn.close()

print("테이블 생성이 완료되었습니다.")
'''

# 값 넣어주기


engine = create_engine('mysql+pymysql://root:a1536613@127.0.0.1:3306/stock_db')
conn = pymysql.connect(host='127.0.0.1', 
                       user='root', 
                       password='a1536613',
                       db='stock_db',
                       charset='utf8')

mycursor = conn.cursor()


ticker_list = pd.read_sql("""
                          select * from kor_ticker
                          where 기준일 =(select max(기준일 ) from kor_ticker)
                          and 종목구분 ='보통주';
                          """, con=engine)

query = """
    insert into kor_price(날짜, 시가, 고가, 저가, 종가, 거래량, 종목코드)
    values (%s, %s, %s, %s, %s, %s, %s) as new
    on duplicate key update
    시가 = new.시가, 고가 = new.고가, 저가 = new.저가, 종가 = new.종가, 거래량 = new.거래량;"""

# 혹시 에러나면 err_list에 에러난 종목 담아두기
err_list=[]


for i in tqdm(range(0,len(ticker_list))):
    #티커 선택
    ticker = ticker_list['종목코드'][i]
    
    #시작일(5년전) 종료일
    fr = (date.today()+relativedelta(years=-5)).strftime("%Y%m%d")
    to  = (date.today()).strftime("%Y%m%d")
    
    # url 생성
    url = f'''https://fchart.stock.naver.com/siseJson.nhn?symbol={ticker}&requestType=1&startTime={fr}&endTime={to}&timeframe=day'''
    
    # 데이터 다운
    data = rq.get(url).content
    data_price = pd.read_csv(BytesIO(data))

    
    # 데이터 클렌징
    price = data_price.iloc[:, 0:6] 
    price.columns = ['날짜', '시가', '고가','저가','종가','거래량']
    price = price.dropna()

    price['날짜'] = price['날짜'].str.extract('(\d+)')
    price['날짜'] = pd.to_datetime(price['날짜'])
    price['종목코드'] = ticker    
    
    
    
    # db 저장
    args = price.values.tolist()
    mycursor.executemany(query, args)
    conn.commit()
    
    time.sleep(2)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    















