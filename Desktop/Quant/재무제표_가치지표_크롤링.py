# 재무제표 크롤링 및 가치지표 계산
# 네이버 증권은 동적 크롤링해야해서 느림

from sqlalchemy import create_engine
import pandas as pd


engine = create_engine('mysql+pymysql://root:a1536613@127.0.0.1:3306/stock_db')

query = '''
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker)
and 종목구분='보통주';

'''

ticker_list = pd.read_sql(query, con=engine)
engine.dispose()

i=1
ticker = ticker_list['종목코드'][i]

url = f'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{ticker}'


# 화면상 보이는 것만 가져오는 것이 아니라 토글? 열어야 보이는 데이터까지 가져오기
data = pd.read_html(url, displayed_only=False, flavor='lxml')

print(data[0].columns.tolist(),  # 연간 기준 포괄손익계산서
      data[2].columns.tolist(),  # 연간 기준 재무 상태표
      data[4].columns.tolist()  # 연간 기준 현금흐름표
      )

data_fs_y = pd.concat([data[0].iloc[:, ~data[0].columns.str.contains('전년동기')],
           data[2],
           data[4]
           ])

# 별도 재무제표는 다른 이름으로 나오므로 통일
data_fs_y = data_fs_y.rename(columns={data_fs_y.columns[0]:'계정'})

# 종목별 결산월을 알아야 연간 재무제표에 해당하는 열을 선택할 수 있음
import requests as rq
from bs4 import BeautifulSoup
import re

page_data = rq.get(url)
page_data_html = BeautifulSoup(page_data.content,'lxml')

fiscal_data = page_data_html.select('div.corp_group1 > h2')
fiscal_data_text = fiscal_data[1].text
fiscal_data_text = re.findall('[0-9]+', fiscal_data_text)



data_fs_y = data_fs_y.loc[:, (data_fs_y.columns=='계정')|
                          (data_fs_y.columns.str[-2:].isin(fiscal_data_text))]


# cleansing 작업
data_fs_y['계정'].value_counts(ascending=False)
# 여러개 중복 존재하는 계정 존재 => 기타, 배당금수익 등 

# ticker는 종목코드, frequency는 연간 or 분기
def clean_fs(df, ticker, frequency):
    df = df[~df.loc[:,~df.columns.isin(['계정'])].isna().all(axis=1)]
    df = df.drop_duplicates(['계정'], keep='first')
    df = pd.melt(df, id_vars='계정', var_name='기준일', value_name='값')
    df = df[~pd.isnull(df['값'])]
    df['계정'] = df['계정'].replace({'계산에 참여한 계정 펼치기': ''}, regex=True)
    df['기준일'] = pd.to_datetime(df['기준일'],
                               format='%Y/%m') + pd.tseries.offsets.MonthEnd()
    df['종목코드'] = ticker
    df['공시구분'] = frequency
    
    return df


data_fs_y_clean = clean_fs(data_fs_y,ticker ,'y')

data_fs_q = pd.concat(
    [data[1].iloc[:,~data[1].columns.str.contains('전년동기')], data[3], data[5]])

data_fs_q = data_fs_q.rename(columns={data_fs_q.columns[0]:'계정'})
data_fs_q_clean = clean_fs(data_fs_q, ticker, 'q')


data_fs_bind = pd.concat([data_fs_y_clean, data_fs_q_clean])



import pymysql
'''
conn = pymysql.connect(host='127.0.0.1', 
                       user='root', 
                       password='a1536613',
                       db='stock_db',
                       charset='utf8')


try:
    # 커서 생성
    with conn.cursor() as cursor:
        # SQL 실행
        cursor.execute("USE stock_db;")
        cursor.execute("""
            CREATE TABLE kor_fs (
                계정 varchar(30),
                기준일 date,
                값 float,
                종목코드 varchar(6),
                공시구분 varchar(1),
               primary key(계정, 기준일, 종목코드, 공시구분)
            );
        """)
        

        conn.commit()

finally:
    # 데이터베이스 연결 종료
    conn.close()

print("테이블 생성이 완료되었습니다.")

'''


from tqdm import tqdm
import time
# 엔진 및 연결 설정
engine = create_engine('mysql+pymysql://root:a1536613@127.0.0.1:3306/stock_db')
conn = pymysql.connect(host='127.0.0.1', user='root', password='a1536613', db='stock_db', charset='utf8')
mycursor = conn.cursor()

# 티커리스트 불러오기
ticker_list = pd.read_sql("""
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker)
and 종목구분 = '보통주';
""", con=engine)

query = """
INSERT INTO kor_fs (계정, 기준일, 값, 종목코드, 공시구분)
VALUES (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 값=VALUES(값);
"""

err_lst = []

for i in tqdm(range(0,len(ticker_list))):
    ticker = ticker_list['종목코드'][i]
    
    try:
        url= f'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{ticker}'
        
        data = pd.read_html(url, displayed_only=False)
        
        data_fs_y = pd.concat([
            data[0].iloc[:,~data[0].columns.str.contains('전년동기')], data[2],
            data[4]
            ])
        
        data_fs_y = data_fs_y.rename(columns={data_fs_y.columns[0]:"계정"})
        
        page_data = rq.get(url)
        page_data_html = BeautifulSoup()(page_data.content, 'html.parser')
                
                
        fiscal_data = page_data_html.select('div.corp_group1 > h2')
        fiscal_data_text = fiscal_data[1].text
        fiscal_data_text = re.findall('[0-9]+', fiscal_data_text)
        
        # 결산년에 해당하는 계정만 남기기
        data_fs_y = data_fs_y.loc[:, (data_fs_y.columns=='계정')|
                                  (data_fs_y.columns.str[-2:].isin(fiscal_data_text))]
        

        
                
        data_fs_y_clean = clean_fs(data_fs_y,ticker ,'y')
        
        data_fs_q = pd.concat(
            [data[1].iloc[:,~data[1].columns.str.contains('전년동기')], data[3], data[5]])
        
        data_fs_q = data_fs_q.rename(columns={data_fs_q.columns[0]:'계정'})
        data_fs_q_clean = clean_fs(data_fs_q, ticker, 'q')
        
        
        data_fs_bind = pd.concat([data_fs_y_clean, data_fs_q_clean])
        
        args = data_fs_bind.values.tolist()
        mycursor.executemany(query,args)
        conn.commit()
        
    except:
        print(ticker)
        err_lst.append(ticker)
        

    time.sleep(2)


conn.close()



























