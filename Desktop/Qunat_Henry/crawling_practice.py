import requests as rq

url = 'https://quotes.toscrape.com/'
quote = rq.get(url)

quote.content

from bs4 import BeautifulSoup
quote html 