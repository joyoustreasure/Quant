#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 15:18:30 2024

@author: choiheejin
"""

# 금융 뉴스 속보 크로링



import requests as rq
from bs4 import BeautifulSoup


url = "https://finance.naver.com/news/news_list.naver?mode=LSS2D&section_id=101&section_id2=258"
news = rq.get(url)


html = BeautifulSoup(news.content, features='lxml')


# news_title = html.select('#contentarea_left > ul > li.newsList.top > dl > dd:nth-child(2) > a')

news_title = html.select('dl > dd.articleSubject>a')

titles = [i['title'] for i in news_title]
titles



#table data
import pandas as pd
url = "https://en.wikipedia.org/wiki/List_of_countries_by_stock_market_capitalization"
tbl = pd.read_html(url)
# tbl 안에 테이블 4개 다 들어가있



#KIND 공시
url = "https://kind.krx.co.kr/disclosure/todaydisclosure.do"
payload ={'method':'searchTodayDisclosureSub',
          'currentPageSize':'15',
          'pageIndex':'1',
          'orderMode':'0',
          'orderStat':'D',
          'marketType':'1',
          'forward':'todaydisclosure_sub',
          'chose':'S',
          'todayFlag':'N',
          'selDate':'2024-05-09'}

data = rq.post(url, data=payload)

# 엑셀 데이터가 html 형태로 들어온ㄹ 것
html = BeautifulSoup(data.content, features='lxml')

#prettify는 다시 unicode로 돌려줌
html_unicode = html.prettify()
html_unicode

tbl = pd.read_html(html_unicode)
tbl