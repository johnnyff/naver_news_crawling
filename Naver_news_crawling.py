
import openpyxl
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import requests
import time
import random

def naver_news_crawling():

    try :
        wb = openpyxl.load_workbook("naver_news.xlsx")
        sheet = wb.active()
    except:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(['날짜','제목','링크','본문'])



    for i in range(180):
        driver = webdriver.Chrome('./chromedriver')
        url_base = 'https://news.naver.com/main/ranking/popularDay.naver?date='

        current_working_date = date.today() - timedelta(i)
        current = current_working_date.strftime("%Y%m%d")
        print("On processing : ",current_working_date)

        url = url_base+current
        driver.get(url)

        while True:
            try:
                button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR ,'div.rankingnews._popularWelBase._persist > button')))
                button.click()
                print("clicked")
            except:
                print("breaked")
                break
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        news = soup.select("#wrap > div.rankingnews._popularWelBase._persist div.rankingnews_box ul.rankingnews_list li div")
        for article in news:
            try:
                temp = []
                temp.append(current_working_date)
                title = article.select_one("a").text
                link_cage = article.select_one("a")
                link = link_cage.attrs['href']
                contents_address ="https://news.naver.com/"+link
                driver.get(contents_address)
                contents = driver.find_element_by_css_selector("#articleBodyContents").text
                temp.append(title)
                temp.append(link)
                temp.append(contents)
                time.sleep(random.random())
                sheet.append(temp)

            except:
                pass
        driver.quit()


        wb.save("naver_news.xlsx")



