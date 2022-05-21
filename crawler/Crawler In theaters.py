import requests
import datetime
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import pymysql
import Ambassador
import ShowTime

engine = create_engine('mysql+pymysql://root:123456@localhost/movielover')

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
movie_info = []
yahoo_id = []
release_date = []
yahoo_posterUrl = []

ambassador_id = []
ambassador_posterUrl = []
today = str(datetime.date.today()).replace('-','/')

showtime_id = []

pageNumber = 1

def Intheaters(pageNum):
    url = "https://movies.yahoo.com.tw/movie_intheaters.html?page="+str(pageNum)
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    
    soup = BeautifulSoup(resp.text, 'lxml')
    titles_ZH = soup.find_all("div", attrs={'class':"release_movie_name"})

    for title in titles_ZH:
        if title.a !=None:
            print(title.a.string)
            yahoo_id.append(title.a["href"][-5:])
            movie_titles_ZH.append(title.a.string.replace('\n','').replace(' ',''))

    titles_EN = soup.find_all("div", attrs={'class':"en"})

    for title in titles_EN:
        if title.a !=None:
            # print(title.a.string)
            movie_titles_EN.append(title.a.string.replace('\n','').replace(' ',''))

    infos = soup.find_all("div", attrs={'class':"release_text"})
    
    for info in infos:
        movie_info.append(info.find('span').text.replace('\n','').replace('\r','').replace(' ',''))

    dates = soup.find_all("div", attrs={'class':"release_movie_time"})

    for date in dates:    
        release_date.append(date.text.replace('\n','').replace('上映日期：','').replace(' ',''))
    
    posters = soup.find_all("div", attrs={'class':"release_foto"})

    for poster in posters:
        yahoo_posterUrl.append(poster.img['data-src'])

    NoMorePage = soup.find("li", attrs={'class':"nexttxt disabled"})
    if NoMorePage:
        return

    pageNum = pageNum+1
    Intheaters(pageNum)

def ThisWeekNew(pageNum):
    url = "https://movies.yahoo.com.tw/movie_thisweek.html?page="+str(pageNum)
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    
    soup = BeautifulSoup(resp.text, 'lxml')
    titles_ZH = soup.find_all("div", attrs={'class':"release_movie_name"})

    for title in titles_ZH:
        if title.a !=None:
            # print(title.a.string)
            yahoo_id.append(title.a["href"][-5:])
            movie_titles_ZH.append(title.a.string.replace('\n','').replace(' ',''))

    titles_EN = soup.find_all("div", attrs={'class':"en"})

    for title in titles_EN:
        if title.a !=None:
            print(title.a.string)
            movie_titles_EN.append(title.a.string.replace('\n','').replace(' ',''))

    infos = soup.find_all("div", attrs={'class':"release_text"})
    
    for info in infos:
        movie_info.append(info.find('span').text.replace('\n','').replace('\r','').replace(' ',''))
    
    dates = soup.find_all("div", attrs={'class':"release_movie_time"})

    for date in dates:    
        release_date.append(date.text.replace('\n','').replace('上映日期：','').replace(' ',''))

    posters = soup.find_all("div", attrs={'class':"release_foto"})

    for poster in posters:
        yahoo_posterUrl.append(poster.img['data-src'])

    NoMorePage = soup.find("li", attrs={'class':"nexttxt disabled"})
    if NoMorePage:
        return

    pageNum = pageNum+1
    ThisWeekNew(pageNum)

def outcome():
    # df_InTheaters_movie = pd.DataFrame()
    # df_InTheaters_movie["中文名"]=movie_titles_ZH
    # df_InTheaters_movie["英文名"]=movie_titles_EN
    # # df_InTheaters_movie_id["簡介"]=movie_info
    # df_InTheaters_movie["上映日"]=release_date
    # df_InTheaters_movie["ID"]=yahoo_id
    # df_InTheaters_movie["海報Url"]=yahoo_posterUrl
    # #存到檔案做備用
    # df_InTheaters_movie.to_csv("./Yahoo Movie/InTheaters_movie_id.csv",encoding="utf-8-sig")

    # df_yahoo = pd.DataFrame(
    #     {   
    #     'movie_name_ZH': movie_titles_ZH,
    #     'movie_name_EN': movie_titles_EN,
    #     'release_date':release_date,
    #     'yahoo_id':yahoo_id,
    #     'poster_url':yahoo_posterUrl
    #     },columns=['movie_name_ZH','movie_name_EN','release_date','yahoo_id','poster_url']
    # )
    # print(df_yahoo)
    # df_yahoo.to_sql('movies', con = engine, if_exists = 'append', index=False)

    for i in range (len(movie_titles_ZH)):
        sql = '''SELECT `movie_name_ZH` FROM `movies` WHERE `movie_name_ZH` = %s'''
        cursor.execute(sql,movie_titles_ZH[i])
        result = cursor.fetchone()
        print(result)
        if result != None:
            sql = '''UPDATE `movies` SET `yahoo_id`=%s, `poster_url`=%s ,`release_date`=%s WHERE `movie_name_ZH` = %s '''
            try:
                cursor.execute(sql,(yahoo_id[i],yahoo_posterUrl[i],release_date[i],movie_titles_ZH[i]))
                conn.commit()
            except:
                conn.rollback()
                print('UP error')
        else:
            sql='''INSERT INTO `movies`(movie_name_ZH,movie_name_EN,yahoo_id,poster_url,release_date) 
            VALUE(%s,%s,%s,%s,%s)'''
            try:
                cursor.execute(sql,(movie_titles_ZH[i],movie_titles_EN[i],yahoo_id[i],yahoo_posterUrl[i],release_date[i]))
                conn.commit()
            except:
                conn.rollback()
                print('IN error')

if __name__ == '__main__':
    Intheaters(pageNumber)
    ThisWeekNew(pageNumber)
    outcome()

Ambassador.AmbassadorData()
ShowTime.showtimeData()
# rerunTime = "05:34"
# print(rerunTime)
# def job(t):
#     print ("I'm working...", t)
#     return
# runtime = "05:44"
# schedule.every().day.at(runtime).do(Intheaters,1)
# schedule.every().day.at(runtime).do(ThisWeekNew,pageNumber)
# schedule.every().day.at(runtime).do(outcome)
# schedule.every().day.at("05:35").do(Ambassador.AmbassadorData)
# schedule.every().day.at("05:35").do(ShowTime.showtimeData)

# while True:
#     schedule.run_pending()
#     time.sleep(3)
