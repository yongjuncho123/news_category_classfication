from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time



# 각 섹션별로(정치 경제 등등)몇 페이지나 있을까?
# 110 페이지까지 크롤링(한 페이지당 20개 기사 한 섹션당 2200개 기사)
pages = [110, 110, 110, 78, 110, 66]
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=1'
# 크롬 브라우저에서 열거야
options = webdriver.ChromeOptions()
options.add_argument('lang=ko_kr')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')

driver = webdriver.Chrome('./chromedriver', options=options)

df_titles = pd.DataFrame()
# for i in range(0, 6):
#      # i는 섹션
#      titles = []
#     for j in range(1, pages[i]+1):
#         url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i, j)
#         driver.get(url)
#         time.sleep(0.2)
#         # j 는 페이지 수
#
#         for k in range(1, 5):
#             # k는 ul 번호
#             for l in range(1, 6):
#                 # l은 li 번호
#                 x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l)
#                 try:
#                     title = driver.find_element_by_xpath(x_path).text
#                     title = re.compile('[^가-힣 ]').sub('', title)
#                     titles.append(title)
#                 except NoSuchElementException as e:
#                     print(e)
#                     print(category[i], j,'page', k * l)
#                 except StaleElementReferenceException as e:
#                     print(e)
#                     print(category[i], j, 'page', k * l)
#                 except:
#                     print('error')
#         if j % 30 == 0:
#             # 데이터가 30페이지까지 크롤링하면 저장
#             print('save', len(titles))
#             df_section_titles = pd.DataFrame(titles, columns=['titles'])
#             df_section_titles['category'] = category[i]
#             df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)  # 합쳐질때 같은 인덱스가 안생기게
#             df_titles.to_csv('./crawling_data_{}_{}_{}.csv'.format(category[i], j- 29, j), index=False)  # 인덱스없이 데이터만 저장
#             titles = []
#     df_section_titles = pd.DataFrame(titles, columns=['titles'])
#     df_section_titles['category'] = category[i]
#     df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)  # 합쳐질때 같은 인덱스가 안생기게
#     df_titles.to_csv('./crawling_data_{}_last.csv'.format(category[i], index=False)  # 인덱스없이 데이터만 저장
#     titles = []
# driver.close() # 크롤링이 끝나면 닫아줘야됨 안되면 창이 계속 켜져있어 계속 저장할거임


# 규칙적으로 숫자가 바뀌니 포문으로 받아오자
# //*[@id="section_body"]/ul[1]/li[2]/dl/dt[2]/a
# //*[@id="section_body"]/ul[1]/li[3]/dl/dt[2]/a
# //*[@id="section_body"]/ul[1]/li[4]/dl/dt[2]/a
# //*[@id="section_body"]/ul[1]/li[5]/dl/dt[2]/a
# //*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[2]/li[3]/dl/dt[2]/a
# //*[@id="section_body"]/ul[2]/li[5]/dl/dt[2]/a

for i in range(0, 2):
    titles = []
    for j in range(1,pages[i]+1):
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i, j)
        driver.get(url)
        time.sleep(0.2)

        for k in range(1, 5):
            for l in range(1, 6):
                x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l)
                try:
                    title = driver.find_element_by_xpath(x_path).text
                    title = re.compile('[^가-힣 ]').sub('', title)
                    titles.append(title)
                except NoSuchElementException as e:
                    time.sleep(0.5)
                    try:
                        title = driver.find_element_by_xpath(x_path).text
                        title = re.compile('[^가-힣 ]').sub('', title)
                        titles.append(title)
                    except:
                        try:
                            x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)
                            title = re.compile('[^가-힣 ]').sub('', title)
                            titles.append(title)
                        except:
                            print('no such element')
                except StaleElementReferenceException as e:
                    print(e)
                    print(category[i], j, 'page', k * l)
                except:
                    print('error')
        if j % 30 == 0:
            df_section_titles = pd.DataFrame(titles, columns=['titles'])
            df_section_titles['category'] = category[i]
            df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
            df_titles.to_csv('./crawling_data_{}_{}.csv'.format(category[i], j), index=False)
            titles = []
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
    df_titles.to_csv('./crawling_data_{}_{}.csv'.format(category[i], j), index=False)
    titles = []
driver.close()

