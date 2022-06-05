
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from sqlalchemy import create_engine
import pymysql

engine = create_engine('mysql+pymysql://root:12345678@localhost/movielover')

host='localhost'
port=3306
user='root'
passwd='12345678'
database='movielover'

conn=pymysql.connect(
    host=host,
    port=port,
    user=user,
    passwd=passwd,
    database=database, 
    charset='utf8'
)

cursor=conn.cursor()
#"上映中"頁面抓取
movie_titles_ZH = []
movie_titles_EN = []
showtime_id = []
release_date = []
showtime_posterUrl = []

# class showtime():

def showtimeData():
    url = 'https://www.showtimes.com.tw/programs'

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, 'lxml')

    allZH = soup.find_all("div", attrs={'class':"sc-khQegj bhNiaF"})
    for title in allZH:
        movie_titles_ZH.append(title.string)

    allEN = soup.find_all("div", attrs={'class':"sc-hUpaCq kBYtxh"})
    for title in allEN:
        movie_titles_EN.append(title.string)

    alldates = soup.find_all("div", attrs={'class':"sc-jgrJph efIpjR"})
    for date in alldates:
        release_date.append(date.find('span').text.replace('/','-'))
    
    showtimeID()

def showtimeID():
    url = 'https://www.showtimes.com.tw/programs'

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    allmovies_count = len(soup.find_all('div', attrs={'class':'sc-khQegj bhNiaF'}))
    print(allmovies_count)

    movie_intheater = soup.find("div", attrs={'class':"sc-jJoQJp jOIJtL"})
    movie_intheater_count = len(movie_intheater.find_all("div", attrs={'class':"sc-AjmGg gxGAhT"}))
    print(movie_intheater_count)
    movie_intheater_allRow = len(movie_intheater.find_all("div", attrs={'class':"d-flex flex-row pb-5 pt-1 flex-grow-1"}))
    print(movie_intheater_allRow)        
    
    j=1
    i=1        
    loop = 1
    for movie in range (allmovies_count):   

        if i == 6:
            j=j+1
            i=1

        if  loop < movie_intheater_count:
            movielist = driver.find_element(by=By.XPATH,value='/html/body/div[2]/div/div[6]/div/div/div['+ str(j) +']/div['+ str(i) +']/div/a')
        elif  loop == movie_intheater_count:
            movielist = driver.find_element(by=By.XPATH,value='/html/body/div[2]/div/div[6]/div/div/div['+ str(j) +']/div['+ str(i) +']/div/a')
            i=0
            j=1
        elif  loop > movie_intheater_count:
            movielist = driver.find_element(by=By.XPATH,value='/html/body/div[2]/div/div[9]/div/div/div['+ str(j) +']/div['+ str(i) +']/div/a')

        movielist.click()
        showtime_id.append(driver.current_url[-5:])
        driver.back()
        i=i+1
        loop=loop+1
        
    outcome()

def outcome():

    # df_Showtime_movie = pd.DataFrame()
    # df_Showtime_movie["中文名"]=movie_titles_ZH
    # df_Showtime_movie["英文名"]=movie_titles_EN
    # df_Showtime_movie["上映日"]=release_date
    # df_Showtime_movie["ID"]=showtime_id

    # # 存到檔案做備用
    # df_Showtime_movie.to_csv("./crawler/ShowTime_movie_id.csv",encoding="utf-8-sig")
    # print(df_Showtime_movie)
    # df_Showtime = pd.DataFrame(
    #     {   
    #     'movie_name_ZH': movie_titles_ZH,
    #     'movie_name_EN': movie_titles_EN,
    #     'release_date':release_date,
    #     'showtime_id':showtime_id,
    #     },columns=['movie_name_ZH','movie_name_EN','release_date','showtime_id']
    # )

    # df_Showtime.to_sql('movies', con = engine, if_exists = 'append', index=True)

    for i in range (len(movie_titles_ZH)):
        sql = '''SELECT `movie_name_ZH` FROM `movies` WHERE `movie_name_ZH` = %s'''
        cursor.execute(sql,movie_titles_ZH[i])
        result = cursor.fetchone()
        print(result)
        if result != None:
            sql = '''UPDATE `movies` SET `showtime_id`=%s, `movie_name_EN`=%s WHERE `movie_name_ZH` = %s '''
            try:
                cursor.execute(sql,(showtime_id[i],movie_titles_EN[i],movie_titles_ZH[i]))
                conn.commit()
            except:
                conn.rollback()
                print('UP error')
        else:
            continue
            # sql='''INSERT INTO `movies`(movie_name_ZH,movie_name_EN,showtime_id,release_date) 
            # VALUE(%s,%s,%s,%s)'''
            # try:
            #     cursor.execute(sql,(movie_titles_ZH[i],movie_titles_EN[i],showtime_id[i],release_date[i]))
            #     conn.commit()
            # except:
            #     conn.rollback()
            #     print('IN error')

if __name__ == '__main__':
    showtimeData()


