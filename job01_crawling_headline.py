from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime


category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
# 네이버 뉴스 정치섹션
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
# 네이버 뉴스 경제섹션
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
# resp = requests.get(url, headers = headers)
# # print(resp)
# # print(resp)
# # print(list(resp))
# # print(type(resp))
# # 뷰티풀 숲은 보기 좋게 바꿔줌
# soup = BeautifulSoup(resp.text, 'html.parser')
# # print(soup)
# # 셀렉터 안에 있는 것만 받는다
# title_tags = soup.select('.cluster_text_headline')
# # print(title_tag)
#
# # hmtl 안 문자열만 보고싶음
# # print(title_tags[0].text)
# # titles = []
# # for title_tag in title_tags:
# #     titles.append(title_tag.text)
#
# #
#
# # 불러온 타이틀로 자연어 학습을 할건데 문장부호들은 별 도움이 안됨 / 또 단어별 조사별로 쪼개서 줘야됨 (협의된 = 협의 / 된) / 조사도 버림 / 의미를 가진 형태소만 학습시킴
#
# # re를 사용해 한글만 남길거임
# titles = []
# for title_tag in title_tags:
#     title = re.compile('[^가-힣 ]').sub('',title_tag.text) # 모든 한글과 띄어쓰기를('[가-힣 ]') 제외한 나머지를 뺀다(sub) , 뺀 자리는 ''로 채움
#     titles.append(title)
#
# print(titles)

# 이제 나머지 경제 문화등 섹션도 다 긁어올 생각이다
df_titles = pd.DataFrame()
for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.cluster_text_headline')
    titles = []
    for title_tag in title_tags:
        title = re.compile('[^가-힣 ]').sub('', title_tag.text)  # 모든 한글과 띄어쓰기를('[가-힣 ]') 제외한 나머지를 뺀다(sub) , 뺀 자리는 ''로 채움
        titles.append(title)
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows',
                          ignore_index=True)
print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())

df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)

# //*[@id="SECTION-LIST"]/ul/li[1]/a[2]
# //*[@id="SECTION-LIST"]/ul/li[2]/a[2]
# //*[@id="SECTION-LIST"]/ul/li[3]/a[2]
# //*[@id="SECTION-LIST"]/ul/li[50]/a[2]
# //*[@id="SECTION-LIST"]/ul/li[49]/a[2]