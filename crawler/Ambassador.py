
import requests
from bs4 import BeautifulSoup

import datetime
from sqlalchemy import create_engine
import pymysql

engine = create_engine('mysql+pymysql://root:123456@localhost/movielover')

host='localhost'
port=3306
user='root'
passwd='123456'
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
ambassador_id = []
release_date = []
ambassador_posterUrl = []
today = str(datetime.date.today()).replace('-','/')

def AmbassadorData():
    url = "https://www.ambassador.com.tw/home/MovieList?Type=1"
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    
    soup = BeautifulSoup(resp.text, 'lxml')
    allmovies = soup.find_all("div", attrs={'class':"title"})

    for movie in allmovies:
        ambassador_id.append(movie.a["href"][-50:-14])
        movie_titles_ZH.append(movie.a.string)
        movie_titles_EN.append(movie.find("p").text)
        if movie.a["href"][-10:] == today:
            release_date.append(None)
        else:
            release_date.append(movie.a["href"][-10:].replace('/','-'))
    
    allposters = soup.find_all("a", attrs={'class':"poster"})

    for poster in allposters:
        ambassador_posterUrl.append(poster.img['src'])
    
    outcome()

def outcome():
    # df_Ambassador_movie = pd.DataFrame()
    # df_Ambassador_movie["中文名"]=movie_titles_ZH
    # df_Ambassador_movie["英文名"]=movie_titles_EN
    # df_Ambassador_movie["上映日"]=release_date
    # df_Ambassador_movie["ID"]=ambassador_movie_id
    # df_Ambassador_movie["海報Url"]=ambassador_posterUrl

    # #存到檔案做備用
    # df_Ambassador_movie.to_csv("./Ambassador/ambassador_movie_id.csv",encoding="utf-8-sig")

    # df_Ambassador = pd.DataFrame(
    #     {   
    #     'movie_name_ZH': movie_titles_ZH,
    #     'movie_name_EN': movie_titles_EN,
    #     'release_date':release_date,
    #     'ambassador_id':ambassador_movie_id,
    #     'poster_url':ambassador_posterUrl
    #     },columns=['movie_name_ZH','movie_name_EN','release_date','ambassador_id','poster_url']
    # )
    # print(df_Ambassador)
    # df_Ambassador.to_sql('movies', con = engine, if_exists = 'append', index=False)
    for i in range (len(movie_titles_ZH)):
        sql = '''SELECT `movie_name_ZH` FROM `movies` WHERE `movie_name_ZH` = %s'''
        cursor.execute(sql,movie_titles_ZH[i])
        result = cursor.fetchone()
        print(result)
        if result != None:
            sql = '''UPDATE `movies` SET `ambassador_id`=%s, `poster_url`=%s ,`release_date`=%s WHERE `movie_name_ZH` = %s '''
            try:
                cursor.execute(sql,(ambassador_id[i],ambassador_posterUrl[i],release_date[i],movie_titles_ZH[i]))
                conn.commit()
            except:
                conn.rollback()
                print('UP error')
        else:
            sql = '''INSERT INTO `movies`(movie_name_ZH,movie_name_EN,ambassador_id,poster_url,release_date) 
            VALUE(%s,%s,%s,%s)'''
            try:
                cursor.execute(sql,(movie_titles_ZH[i],movie_titles_EN[i],ambassador_id[i],ambassador_posterUrl[i],release_date[i]))
                conn.commit()
            except:
                conn.rollback()
                print('IN error')

if __name__ == '__main__':
    AmbassadorData()