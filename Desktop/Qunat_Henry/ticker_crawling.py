# 국내 주식 티커 및 섹터 데이터 크롤링하기

import requests as rq
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/sise/sise_deposit.naver'
data = rq.get(url)
data_html = BeautifulSoup(data.content,'lxml')

parse_day = data_html.select_one(
    'div.subtop_sise_graph2 >ul.subtop_chart_note > li > span.tah').text
parse_day

import re

biz_day = re.findall('[0-9]+', parse_day)
biz_day = ''.join(biz_day)

biz_day


# 티커 크롤링
# 어떠한 종목이 상장되어있는가에 대한 정보
import requests as rq
from io import BytesIO
import pandas as pd

# 아래 gen_otp_stk에서 mktId만 'KSQ'로 바꾸면 코스닥. 'STK'는 코스피
gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
gen_otp_stk = {
    'mktId': 'STK',
    'trdDd': biz_day,
    'money':'1',
    'csvxls_isNo': 'false',
    'name':'fileDown',
    'url':'dbms/MDC/STAT/standard/MDCSTAT03901'}


# Referer란 링크를 통해서 각가의 웹사이트로 방문할때 남는 흔적
headers = {'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201'}

otp_stk = rq.post(gen_otp_url, gen_otp_stk, headers = headers).text


down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
down_sector_stk = rq.post(down_url, {'code':otp_stk}, headers=headers)
sector_stk = pd.read_csv(BytesIO(down_sector_stk.content), encoding='EUC-KR', on_bad_lines='skip')
sector_stk

#코스닥.
gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
gen_otp_ksq = {
    'mktId': 'KSQ',
    'trdDd': biz_day,
    'money':'1',
    'csvxls_isNo': 'false',
    'name':'fileDown',
    'url':'dbms/MDC/STAT/standard/MDCSTAT03901'}


# Referer란 링크를 통해서 각가의 웹사이트로 방문할때 남는 흔적
headers = {'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201'}

otp_ksq = rq.post(gen_otp_url, gen_otp_ksq, headers = headers).text


down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
down_sector_ksq = rq.post(down_url, {'code':otp_stk}, headers=headers)
sector_ksq = pd.read_csv(BytesIO(down_sector_ksq.content), encoding='EUC-KR', on_bad_lines='skip')
sector_ksq


# 코스피 + 코스닥
krx_sector = pd.concat([sector_stk,sector_ksq]).reset_index(drop=True)
krx_sector


# 종목명에 공백이 있는 경우를 cleansing
krx_sector['종목명'] = krx_sector['종목명'].str.strip()

krx_sector['기준일'] = biz_day






# 개별종목 지표 다운

gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
gen_otp_data = {
    'searchType':'1',
    'mktId':'ALL',
    'trdDd':biz_day,
    'csvxls_isNo':'false',
    'name':'fileDown',
    'url': 'dbms/MDC/STAT/standard/MDCSTAT03501'   
    }


# Referer란 링크를 통해서 각가의 웹사이트로 방문할때 남는 흔적
headers = {'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201'}

otp = rq.post(gen_otp_url, gen_otp_data, headers = headers).text


down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
krx_idx = rq.post(down_url, {'code':otp}, headers=headers)
krx_idx = pd.read_csv(BytesIO(krx_idx.content), encoding='EUC-KR', on_bad_lines='skip')
krx_idx['종목명'] = krx_idx['종목명'].str.strip()
krx_idx['기준일'] = biz_day

# 하나의 셋에만 존재하는 데이터 => 선박펀드,광물펀드, 해외종목 등 일반적이지 않은 종목에서 드러남
set(krx_sector['종목명']).symmetric_difference(set(krx_idx['종목명']))



# 티커 데이터 생성 및 클렌징
kor_ticker = pd.merge(krx_sector,
                      krx_idx,
                      on = krx_sector.columns.intersection(krx_idx.columns).tolist(),
                      how = 'outer'
                      )



# 스팩 찾기
kor_ticker[kor_ticker['종목명'].str.contains('스팩|제[0-9]+호')]['종목명']


# 우선주 찾기 => 국내 종목 중 종목코드 끝이 0이 아닌 종목은 우선주, 나머지는 일반주
kor_ticker[kor_ticker['종목코드'].str[-1:]!='0']['종목명']

# 리츠 종목
kor_ticker[kor_ticker['종목명'].str.endswith('리츠')]['종목명']



import numpy as np
diff = list(set(krx_sector['종목명']).symmetric_difference(krx_idx['종목명']))

kor_ticker['종목구분'] = np.where(kor_ticker['종목명'].str.contains('스팩|제[0-9]+호'),'스팩',
                              np.where(kor_ticker['종목코드'].str[-1:]!='0','우선주',
                                       np.where(kor_ticker['종목명'].str.endswith('리츠'),'리츠',
                                                np.where(kor_ticker['종목명'].isin(diff), '기타',
                                                         '보통주'))))

kor_ticker = kor_ticker.reset_index(drop = True)
kor_ticker.columns = kor_ticker.columns.str.replace(' ', '')
kor_ticker.columns
kor_ticker = kor_ticker[['종목코드', '종목명', '시장구분', '종가', '시가총액', '기준일', 'EPS', 'BPS', '주당배당금', '종목구분']]

# nan은 SQL에 저장 불가하므로 None으로 바꿔주기
kor_ticker = kor_ticker.replace({np.nan:None})









































