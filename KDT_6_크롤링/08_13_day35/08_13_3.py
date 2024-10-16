# from selenium import webdriver
# import time

# driver = webdriver.Chrome()
# driver.get("https://www.selenium.dev/selenium/web/web-form.html")

# print(driver.title)
# print(driver.page_source)
# time.sleep(2)
# driver.quit()

# #---------------------------------------------------------------
# # selenium api : element

# from selenium import webdriver
# from selenium.webdriver.common.by import By 

# driver = webdriver.Chrome()

# driver.get('http://www.pythonscraping.com/pages/warandpeace.html')
# driver.implicitly_wait(5)

# name = driver.find_element(By.CLASS_NAME, 'green')
# print(name.text)

# print('-'*20)

# name_list = driver.find_elements(By.CLASS_NAME, "green")
# for name in name_list:
#     print(name.text)

# driver.quit()

# # -------------------------------------------------------
# # 네이버 로그인 

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time 

# agent_option = webdriver.ChromeOptions()
# user_agent_string = 'Mozilla/5.0'
# agent_option.add_argument('user-agent='+user_agent_string)

# driver = webdriver.Chrome(options = agent_option)
# driver.get('https://nid.naver.com/nidlogin.login')

# driver.find_element(By.NAME, 'id').send_keys('아이디')
# driver.find_element(By.NAME,'pw').send_keys('패스워드!')

# driver.find_element(By.ID, 'log.login').click()
# time.sleep(3)
# driver.quit()

# # --------------------------------------------------------------
# # 구글 검색어 입력 및 검색 결과 

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time 

# driver = webdriver.Chrome()
# driver.get("https://www.google.com/search?q="	+	'Python')

# driver.implicitly_wait(3)

# search_results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf')
# print(len(search_results))

# for result in search_results:
#     title_element = result.find_element(By.CSS_SELECTOR, 'h3')
#     title = title_element.text.strip()
#     print(f'{title}')

# driver.quit()

# # ----------------------------------------------------------
# # selenium api 프레임 이동 

# from bs4 import BeautifulSoup
# from selenium import webdriver
# import	collections
# if	not	hasattr(collections,'Callable'):
# 	collections.Callable =	collections.abc.Callable

# driver = webdriver.Chrome()
# driver.get('https://blog.naver.com/swf1004/221631056531')

# driver.switch_to.frame('mainFrame')

# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')

# results = soup.find_all('div',{'class':'se-module'})

# result1 = []

# for result in results:
#     remove_carriage_str = result.text.replace('\n','')
#     print(remove_carriage_str)
#     result1.append(remove_carriage_str)

# --------------------------------------------------------------
# 잡플래닛 평점 크롤링 

import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd 
from tabulate import tabulate 

company_dict =	{'삼성전자':'https://www.jobplanet.co.kr/companies/30139/reviews/삼성전자',
                'LG전자':'https://www.jobplanet.co.kr/companies/19514/reviews/lg전자',
                'SK하이닉스':'https://www.jobplanet.co.kr/companies/20561/reviews/에스케이하이닉스',
                '네이버':'https://www.jobplanet.co.kr/companies/42217/reviews/네이버'}

xpath_dict =	{'전체평점':'//*[@id="premiumReviewStatistics"]/div[2]/div[1]/div/div[1]/div[1]/span[1]',
                '복지':	'//*[@id="premiumReviewStatistics"]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[2]/span[2]',
                '업무와 삶의 균형':'//*[@id="premiumReviewStatistics"]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[2]/div[2]/span[2]',
                '사내문화':'//*[@id="premiumReviewStatistics"]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[3]/div[2]/span[2]',
                '승진 기회':'//*[@id="premiumReviewStatistics"]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[4]/div[2]/span[2]',
                '경영진':'//*[@id="premiumReviewStatistics"]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[5]/div[2]/span[2]'}

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

company_score_dict = {}
for company_name in company_dict.keys():
    score_list=[]
    company_url = company_dict.get(company_name)
    driver.get(company_url)

    company = driver.find_element(By.CLASS_NAME,'name').text
    print('-'*50)
    print(company)

    for key in xpath_dict.keys():
        point = driver.find_element(By.XPATH, xpath_dict.get(key)).text
        print(f'{key} : {point}', end = ' ')
        score_list.append(point)
    print()

    company_score_dict[company_name] = score_list
    print('company_score_dict')

    for key in company_score_dict.keys():
        print(f'{key} : {company_score_dict.get(key)}')

    columns = ('전체평점','복지','업무와 삶의 균형','사내문화','승진 기회','경영진')

    company_score_df = pd.DataFrame.from_dict(company_score_dict, orient='index',columns=columns)

    print(tabulate(company_score_df, headers='keys',tablefmt='psql'))