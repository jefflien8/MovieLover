import requests
import datetime
# import schedule
# import time
from bs4 import BeautifulSoup
from sqlalchemy import *
import pymysql
import pandas as pd
import re
# import Ambassador
# import ShowTime
# import YahooTheaters

engine = create_engine('mysql+pymysql://admin:password/movielover',echo = True)

host=''
port=3306
user='admin'
passwd='password'
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
            # print(title.a["href"].split('-')[1:-1])
            yahoo_id.append(title.a["href"].split('-')[-1])
            # print(title.a.string.replace('\n',''))
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
            yahoo_id.append(title.a["href"].split('-')[-1])
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
    # df_InTheaters_movie.to_csv("./crawler/InTheaters_movie_id.csv",encoding="utf-8-sig")

    meta = MetaData()

    movies = Table('movies', meta, 
        Column('index', Integer,autoincrement=True), 
        Column('movie_name_ZH', String(255),primary_key = True,nullable=False), 
        Column('movie_name_EN', String(255), nullable=False),
        Column('yahoo_id', String(255),primary_key = True,),
        Column('ambassador_id', String(255)),
        Column('showtime_id', String(255)),
        Column('poster_url', String(255)),
        Column('release_date', Date),
        Column('movie_info', String(5100))
    )

    meta.drop_all(engine, tables=None, checkfirst=True)
    movies.create(engine, checkfirst=True)

    df_yahoo = pd.DataFrame(
        {   
        'movie_name_ZH': movie_titles_ZH,
        'movie_name_EN': movie_titles_EN,
        'yahoo_id':yahoo_id,
        'poster_url':yahoo_posterUrl,
        'release_date':release_date,
        'movie_info':movie_info
        },columns=['movie_name_ZH','movie_name_EN','release_date','yahoo_id','poster_url','movie_info']
    )
    print(df_yahoo)

    df_yahoo.to_sql('movies', con = engine, if_exists = 'append', index=True)

    # for i in range (len(movie_titles_ZH)):
    #     sql = '''SELECT `movie_name_ZH` FROM `movies` WHERE `movie_name_ZH` = %s'''
    #     cursor.execute(sql,movie_titles_ZH[i])
    #     result = cursor.fetchone()
    #     print(result)
    #     if result != None:
    #         sql = '''UPDATE `movies` SET `yahoo_id`=%s, `poster_url`=%s ,`release_date`=%s WHERE `movie_name_ZH` = %s '''
    #         try:
    #             cursor.execute(sql,(yahoo_id[i],yahoo_posterUrl[i],release_date[i],movie_titles_ZH[i]))
    #             conn.commit()
    #         except:
    #             conn.rollback()
    #             print('UP error')
    #     else:
    #         sql='''INSERT INTO `movies`(movie_name_ZH,movie_name_EN,yahoo_id,poster_url,release_date) 
    #         VALUE(%s,%s,%s,%s,%s)'''
    #         try:
    #             cursor.execute(sql,(movie_titles_ZH[i],movie_titles_EN[i],yahoo_id[i],yahoo_posterUrl[i],release_date[i]))
    #             conn.commit()
    #         except:
    #             conn.rollback()
    #             print('IN error')

# if __name__ == '__main__':
#     Intheaters(pageNumber)
#     ThisWeekNew(pageNumber)
    # outcome()

area_id = 28
today = datetime.date.today()
dayCheck = int(1)

theater_list = []
cate_list= []
schedule_list = []
date_list = []
movieScreening_list = []
yahoo_screening = []

def alldata():
    for movie in yahoo_id:
        print(movie)
        yahooplay(movie)
        
    outcome2()

def yahooplay(movie):
    global today,dayCheck
    print (dayCheck)
    if dayCheck == 6:
        today = datetime.date.today()
        dayCheck = 1
        print (dayCheck)
        return
    url = "https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie"

    payload = {'movie_id':movie,
        'date':today,
        'area_id':str(area_id),
        'theater_id':'',
        'datetime':'',
        'movie_type_id':''}
    print(today)
    resp = requests.get(url, params=payload)
    json_data = resp.json()

    soup = BeautifulSoup(json_data['view'],'lxml')
    
    # nodata = soup.find_all("p", attrs={'class':'no_released'})



    # print(html_elem) 
    html_elem = soup.find_all("ul", attrs={'data-theater_name':re.compile(".*")})

    #每個the就是一間戲院
    for the in html_elem:
        # print(the)
        theater = the.find("li",attrs={"class":"adds"})
        # print(theater)
        # print("電影院： {}".format(theater.find("a").text))
    #info裡面分別包含每一間戲院的場次資訊
        info = the.find_all(class_="gabtn")
        # print(info)
        for i in info:
            # print(i)
            # print(i["data-movie_time"],i["data-movie_type"],today)
            movieScreening_list.append(i["data-movie_title"])
            # print(i["data-movie_title"])
            theater_list.append(theater.find("a").text)
            if i["data-movie_time"][0:2] == '00':
                i["data-movie_time"] ='24:'+ i["data-movie_time"][-2:]
                print(i["data-movie_time"])
            if i["data-movie_time"][0:2] == '01':
                i["data-movie_time"] ='25:'+ i["data-movie_time"][-2:]
                print(i["data-movie_time"])
            schedule_list.append(i["data-movie_time"])
            cate_list.append(i["data-movie_type"])
            date_list.append(today)
            yahoo_screening.append(movie)
            
        # print("====================")    
    
    today = today + datetime.timedelta(days = 1) 
    dayCheck = dayCheck+1
    yahooplay(movie)

def outcome2():
    # df = pd.DataFrame()

    # df["片名"] = movieScreening_list
    # df["戲院"] = theater_list
    # df["類型"] = cate_list
    # df["時刻"] = schedule_list
    # df["日期"] = date_list

    # print(df)
    # df.to_csv(".crawler/All_movie_schedule.csv",encoding="utf-8-sig")

    meta = MetaData()

    yahooscreenings = Table('yahooscreenings', meta, 
        # Column('movie_name_ZH', String(255), primary_key = True), 
        Column('yahoo_index', Integer,primary_key = True,autoincrement=True),
        Column('yahoo_id', String(255), nullable=False),
        Column('theater', String(255), nullable=False),
        Column('date', String(255), nullable=False),
        Column('time', String(255), nullable=False),
        Column('type', String(255), nullable=False),
    )

    # meta.drop_all(engine, tables=None, checkfirst=True)
    # yahooscreenings.drop(engine, checkfirst=False)
    yahooscreenings.create(engine, checkfirst=True)

    df_yahooSrceenings = pd.DataFrame(
        {   
        # 'movie_name_ZH': movieScreening_list,
        'yahoo_id':yahoo_screening,
        'theater': theater_list,
        'date':date_list,
        'time':schedule_list,
        'type':cate_list
        },
        columns=['yahoo_id','theater','date','time','type']
    )
    print(df_yahooSrceenings)
    df_yahooSrceenings.to_sql('yahooscreenings', con = engine, if_exists = 'append', index=False)


if __name__ == '__main__':
    Intheaters(pageNumber)
    ThisWeekNew(pageNumber)
    outcome()
    # Ambassador.AmbassadorData()
    # ShowTime.showtimeData()
    alldata()

# runtime = "01:00"
# schedule.every().day.at(runtime).do(Intheaters,pageNumber)
# schedule.every().day.at(runtime).do(ThisWeekNew,pageNumber)
# schedule.every().day.at(runtime).do(outcome)
# schedule.every().day.at(runtime).do(Ambassador.AmbassadorData)
# schedule.every().day.at(runtime).do(ShowTime.showtimeData)
# schedule.every().day.at(runtime).do(alldata)

# while True:
#     schedule.run_pending()
#     time.sleep(3)
#     print('waiting...')
