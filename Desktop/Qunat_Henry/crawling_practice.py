import requests as rq

url = 'https://quotes.toscrape.com/'
quote = rq.get(url)
# html 정보가 담김
# print(quote.content)


# html을 보기 좋게 가공
from bs4 import BeautifulSoup
quote_html = BeautifulSoup(quote.content, features='lxml')


# 명언에 해당하는 부분은 class="quote"인 div태그 하에서, class="text"인 span 태그
quote_div = quote_html.find_all('div', class_ = "quote")

quote_span = quote_div[0].find_all('span', class_="text")[0].text

[i.find_all('span', class_ = 'text')[0].text for i in quote_div]

quote_text = quote_html.select('div.quote > span.text')

texts = [i.text for i in quote_text]

quote_author = quote_html.select('div.quote > span > small.author')

authors = [i.text for i in quote_author]

quote_link = quote_html.select('div.quote > span > a')
links = [i['href'] for i in quote_link]

