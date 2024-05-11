# 동적 크롤링


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

# 드라이버 초기화
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 네이버 접속
url = "https://www.naver.com"
driver.get(url)

# 페이지 소스 가져오기
html_content = driver.page_source

# '뉴스' 링크 클릭
news_link = driver.find_element(By.LINK_TEXT, '뉴스')
#news_link.click()

# 검색창 찾아서 검색하기
# 클래스 이름이 올바른지 확인 필요 (예제에서는 가정한 클래스 이름 사용)
search_input = driver.find_element(By.ID, 'query')  # 네이버 검색창의 ID는 'query'입니다.
search_input.send_keys('퀀트 투자 포트폴리오 만들기')

# 검색 버튼을 찾아 검색 실행
try:
    search_button = driver.find_element(By.ID, 'search-btn')  # 검색 버튼의 ID가 맞는지 확인 필요
    search_button.click()
except Exception as e:
    # ID가 맞지 않을 경우, JavaScript를 사용해 클릭 시도
    driver.execute_script("document.getElementById('search_btn').click();")
    
# 검색창 지우고 다른 검색어 검색
driver.find_element(By.CLASS_NAME, value='box_window').clear()
driver.find_element(By.CLASS_NAME, value='box_window').send_keys('월드퀀트')
driver.find_element(By.CLASS_NAME, value='bt_search').click()




# 다른 탭 눌러보기
driver.find_element(By.XPATH, value = '//*[@id="lnb"]/div[1]/div/div[1]/div/div[1]/div[1]/a').click()


# 페이지 다운
driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
#driver.find_element(By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)

prev_height = driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
    
    curr_height = driver.execute_script('return document.body.scrollHeight')
    if curr_height == prev_height:
        break
    prev_height=curr_height
time.sleep(2)


# 제목 정보 크롤링해오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
txt = soup.find_all('a', class_='title_link')  # 뉴스 제목에 해당하는 클래스 이름이 'news_tit'인 경우
txt_list = [i.text for i in txt]
print(txt_list)





# 드라이버 종료
driver.quit()
