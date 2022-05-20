# import requests
import re
import time
from multiprocessing.sharedctypes import Value
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

#"上映中"頁面抓取
# url = "https://movies.yahoo.com.tw/movie_intheaters.html"
# resp = requests.get(url)
# resp.encoding = 'utf-8'

# soup = BeautifulSoup(resp.text, 'lxml')
# movieTitles = soup.find_all("div", attrs={'class':"release_movie_name"})

# for title in movieTitles:
#     if title.a !=None:
#         print(title.a.string)

url = "https://movies.yahoo.com.tw"

driver = webdriver.Chrome()
driver.get(url)
movieForm = driver.find_element(By.ID,'sbox_mid')
movieForm.click()
time.sleep(3)


soup = BeautifulSoup(driver.page_source, 'lxml')

movie_html = soup.find("select", attrs={'name':'movie_id'})
# print(movie_html)
movie_item = movie_html.find_all("option",attrs={'data-name':re.compile('.*')})
# print(movie_item)

title_list = []
id_list = []
#先宣告兩個list放電影標題跟電影ＩＤ
#因為moite_item 是一個bs4的元素集合，我們要用遍歷去探索它:
for info in movie_item:
    #  print(info)
    #  print(type(info))
    # print("Movie: {}, ID: {}".format(info["data-name"], info["value"]))
    id_list.append(info["value"])
    title_list.append(info["data-name"])
# print(title_list)
# print(id_list)

df_movie_id = pd.DataFrame()
df_movie_id["電影"]=title_list
df_movie_id["ID"]=id_list
#存到檔案做備用
df_movie_id.to_csv("./movie_id.csv",encoding="utf-8-sig")
