# 섹터 크롤링

# 섹터 정보 크롤링

#url ='https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20240510&sec_cd=G10'
# dt는 날짜, sec_cd는 섹터 코드.
# json 파일로 들어가있

import json
import requests as rq
import pandas as pd
from tqdm import tqdm
import time


sector_code = ['G25','G35','G50','G40','G10','G20','G55','G30','G15','G45']

data_sector=[]

for i in tqdm(sector_code):
    url = f'''https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt={biz_day}&sec_cd={i}'''
    data = rq.get(url).json()
    
    # data는 딕셔너리로 존재. dict_keys=['info', 'list', 'sector', 'size']
    # 이중 섹터 구성 종목인 list와 섹터 코드인 sector가 중
    data_pd = pd.json_normalize(data['list'])
    
    data_sector.append(data_pd)
    time.sleep(2)


kor_sector = pd.concat(data_sector, axis=0)
kor_sector = kor_sector[['IDX_CD', 'CMP_CD', 'CMP_KOR', 'SEC_NM_KOR']]
kor_sector['기준일'] = biz_day
kor_sector['기준일'] = pd.to_datetime(kor_sector['기준일'])


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
            CREATE TABLE kor_sector (
                IDX_CD VARCHAR(3),
                CMP_CD VARCHAR(6),
                CMP_KOR VARCHAR(20),
                SEC_NM_KOR VARCHAR(10),
                기준일 DATE,
                PRIMARY KEY(CMP_CD, 기준일)
            );
        """)
        

        conn.commit()

finally:
    # 데이터베이스 연결 종료
    conn.close()

print("테이블 생성이 완료되었습니다.")



# 값 넣어주기
conn = pymysql.connect(host='127.0.0.1', 
                       user='root', 
                       password='a1536613',
                       db='stock_db',
                       charset='utf8')

mycursor = conn.cursor()
query= f"""
    insert into kor sector (IDX_CD, CMP_CD, CMP_KOR, SEC_NM_KOR, 기준일)
    values (%s, %s, %s, %s, %s) as new
    on duplicate key update
    IDX_CD = new.IDX_CD, CMP_KOR = new.CMP_KOR, SEC_NM_KOR = new.SEC_NM_KOR
    """

args = kor_sector.values.tolist()
conn.commit()

conn.close()