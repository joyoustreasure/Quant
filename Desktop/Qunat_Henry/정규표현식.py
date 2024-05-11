# 정규 표현식
import re

data = '동 기업의 매출액은 전년 대비 29.2% 늘어났습니다.'
 
re.findall('\d+.\d+%', data)

# 대괄호 [] 안에 포함된 문자들 중 하나라도 매치되면 
# [ae] => apple, blueberry 등은 매치 됨

# []안에 하이픈 있으면 두 문자 사이 범위
# [a-e]는 [abcde]와 동일, [0-5]는 [012345]와 동일

# [] 안의 ^는 반대를 의미
# [^0-9]는 숫자를 제외한 문자만 매치
# [^abc]는 a,b,c를 제외한 모든 문자와 매


# \d : 숫자와 매치. [0-9]와 동일한 표현식
# \D : 숫자가 아닌 것과 매치. [^0-9]와 동일한 표현식
# \s : whitespace(공백) 문자와 매치. [\t\n\r\f\v]와 동일
# \S : whitespace(공백) 아닌 문자와 매치. [^\t\n\r\f\v]와 동일
# \w : 문자+숫자와 매치. [a-zA-Z0-9]와 동일
# \W : 문자+숫자와 매치. [a-zA-Z0-9]와 동일

# Dot(.)는 줄바꿈 문자 \n을 제외한 모든 문자와 매치 됨
# Dot 하나당 임의의 한 문자 나타냄
# a.e는 'a+모든문자+e'의 형태로써, a와 e 사이 어떤 문자가 들어가도 모두 매치됨
# 'abe', 'ace'는 매치. 'abate'. 'ae'는 매치 안됨


# *의 경우 * 바로 앞에 있는 문자가 0부터 무한대로 반복될 수 있음
# ex. ca*t일 때, ct, cat, caat, caaat 모두 매치

# +의 경우 최소 한번 이상 반복될 때 사
# ca+t 일 경우 ct는 매치 안됨

# {}를 활용하면 반복 횟수 고
# {m,n}은 반복 횟수가 m부터 n까지로 고정
# m 또는 n은 생략 가능
# {3,}의 경우 반복 횟수가 3 이상
# {,3}의 경우 반복 횟수가 3 이

# ?의 경우 {0,1}과 동일. 즉 ? 앞에 문자가 있어도 되고 없어도 된다는 의미


# 정규식 method
# match() : 시작부터 일치하는 패턴 찾음
# search() : 첫번째로 일치하는 패턴 찾음
# findall() : 일치하는 모든 패턴 찾음
# finditer() : findall()과 동일하지만 반복 가능한 객체 반환

p = re.compile('[a-z]+')
# print(type(p))

m = p.match('python')
m
m.group()

p.match('Use python')  # None. 시작이 대문자라서 매치 안되고
# print(p.search('Use python'))  # se


 

p = re.compile('[A-Z]+')
p.match('PYTHON')

#가~힣 은 모든 한글 의미
p = re.compile('[가-힣]+')
p.match('파이썬')



p = re.compile('[a-zA-Z]+')
m = p.findall('Life is too short, You need Python')
m


p = re.compile('[a-zA-Z]+')
m = p.finditer('Life is too short, You need Python')
print(m)
for i in m:
    print(i)
    
    
    
dt = '> 오늘의 날짜는 2022.12.31 입니다.'
p = re.compile('[0-9]+.[0-9]+.[0-9]+')
p.findall(dt)