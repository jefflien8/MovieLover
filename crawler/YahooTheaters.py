from time import time
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime

yahoo_id = []
area_id = 28
today = datetime.date.today()

theater_list = []
cate_list= []
schedule_list = []
date_list = []

def GG():
    url = 'https://movies.yahoo.com.tw/movietime_result.html'
    payload = {'movie_id':str(movie_id), 'area_id':str(area_id)}
    headers = {
        'authority': 'movies.yahoo.com.tw',
        'method': 'GET',
        'path':"/ajax/get_schedule_by_movie?movie_id=" + str(movie_id),
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': 'rxx=28u37rf2vef.2mt2knqz&v=1; _ga=GA1.3.1331628063.1644762582; A1=d=AQABBNQVCWICEL4Q4DhAgFOc2L5Qve0kW1gFEgEBBgGdE2LqYr3Lb2UB_eMBAAcI1BUJYu0kW1g&S=AQAAAh-IwUDGWlV6di22ZqFdBBc; A3=d=AQABBNQVCWICEL4Q4DhAgFOc2L5Qve0kW1gFEgEBBgGdE2LqYr3Lb2UB_eMBAAcI1BUJYu0kW1g&S=AQAAAh-IwUDGWlV6di22ZqFdBBc; GUC=AQEBBgFiE51i6kIf4QSU; BX=5gmp4tlh0i5ek&b=3&s=ks; _ga=GA1.4.1331628063.1644762582; _gid=GA1.4.2130064037.1652007883; A1S=d=AQABBNQVCWICEL4Q4DhAgFOc2L5Qve0kW1gFEgEBBgGdE2LqYr3Lb2UB_eMBAAcI1BUJYu0kW1g&S=AQAAAh-IwUDGWlV6di22ZqFdBBc&j=WORLD; avi=eyJpdiI6IndsQTZKeXNwRVo4c0dUNU02RWlwQ0E9PSIsInZhbHVlIjoiVDdnWDJXRTN1SW9nRFpaUkJqTDVobVpxYnU1M0NwbDJDek9nTXVtVnNjV3UrN0MwTXBEZzgybGlLQ0Znb29HYiIsIm1hYyI6ImE1NDA2NDJiYzU5MTg1MzdkNDlkNDU1MDQxNjk2ZDFkYjJkYTM0ZjIyODdhMGNhNmNiNWMyZmQ2Nzc1YTI4ODAiLCJ0YWciOiIifQ%3D%3D; _gid=GA1.3.2130064037.1652007883; cmp=t=1652207866&j=0&u=1---; b_m2=eyJpdiI6IjdwbFMzL1dIbDM3bktKMGpjZWpJbVE9PSIsInZhbHVlIjoiNEF4T1RreHhGbFRrc2VHaENoWjA1RTdKbzZMTjNTYnVhaXlvSFVUbEdEWnpHT211TDRSZ0FZcGdibkthZ3VwcCtjNTRmNXIwWFI4QWIzQUpxZUFUZ3lTN241QUhldE9VYkNmdGdIT1IzWFBNT1BLN2dxQW1rTDh3dkovdEJpclQiLCJtYWMiOiJjYzRhOTBmYTYwN2U1ZjVmNjg4ZjkwNzNlNjJlZmVkMWQyMWFjMDRmMmNjZTA5OTI0ZGUxM2YyMDc5ZGFiNzdlIiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6IjVYTXhyaGNaclNjbW5mN1RuQzB5SGc9PSIsInZhbHVlIjoiRUM0Tk9sWXJZZFJESytqZDBQTDBEUDBHc2M3c21ad2tJVlA3U2hyb2JoUmhock53dDNSOEZxd01nOW5MSnBzNDBtQ0dHYWZWUk5FUnp0dkR3MXB6dWJ6NGEzNHo5ZmN0M0txZWo0RmtvVTVMLzFrMmRKdUl6ZkwrbDUwL09PbjciLCJtYWMiOiI0ZGI1ZjcxYmU0MjAwNDcwNWQ5MGRlYmRhNjdmMmEwMGU1Y2ZjNDJhYWMwN2UzZDhmZDQwMjdhZjgwZjY4ZjU3IiwidGFnIjoiIn0%3D; ms55=eyJpdiI6IlltaDVTaVJSRHM3VC8xaTM0NG83L2c9PSIsInZhbHVlIjoiTEoyNUNRZlBxdnM0bENqZVZja29iNFFFYm5QTkgza1NaVXR5eEpZLzlDS21YSHRXRjMvYmVHZ2pSZmxNSXNmMWJQWmh6NnlXb0R4NERRYm02RWIyS0U3L2Jhci9TRkk3RlluM2d4TEJ1Z1p5UHRhNmRHd2UzT2NveFI1Y2Z3a0wiLCJtYWMiOiJkOWQ3ZDA0ODMxYWUzMTBjY2I0Mzk4MzA2NTk5M2UxNWQ2ZWFkNGMwMmVmNjZkYzYxOTA4Y2FjYTJmNzE0ODY2IiwidGFnIjoiIn0%3D',
        'referer': 'https://movies.yahoo.com.tw/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Mobile Safari/537.36 Edg/101.0.1210.39',
    }

    resp = requests.get(url, params=payload)
    resp.encoding = 'utf-8'
    # print(resp.url)

    soup = BeautifulSoup(resp.text, 'lxml')
    movie_date = soup.find_all("label", attrs={'for':re.compile("date_[\d]")})
    # print(movie_date)
    # 遍歷movie_date，輸出播放日期
    for date in movie_date:
        print("{} {}".format(date.p.string, date.h3.string))

def alldata():
    for movie in yahoo_id:
        yahooplay(movie)
        print(movie)
    outcome()


def yahooplay(movie):
    global today
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
    
    nodata = soup.find_all("p", attrs={'class':'no_released'})
    if nodata:
        today = datetime.date.today()
        return
    # print(html_elem) 
    html_elem = soup.find_all("ul", attrs={'data-theater_name':re.compile(".*")})

    #每個the就是一間戲院
    for the in html_elem:
        # print(the)
        theater = the.find("li",attrs={"class":"adds"})
        # print(theater)
        print("電影院： {}".format(theater.find("a").text))
    #info裡面分別包含每一間戲院的場次資訊
        info = the.find_all(class_="gabtn")
        # print(info)
        for i in info:
            # print(i)
            print(i["data-movie_time"],i["data-movie_type"],today)
            theater_list.append(theater.find("a").text)
            schedule_list.append(i["data-movie_time"])
            cate_list.append(i["data-movie_type"])
            date_list.append(today)

        print("====================")    
    
    today = today + datetime.timedelta(days = 1) 
    yahooplay(movie)

def outcome():

    df = pd.DataFrame()

    df["戲院"] = theater_list
    df["類型"] = cate_list
    df["時刻"] = schedule_list
    df["日期"] = date_list

    print(df)
    df.to_csv("./movie_schedule.csv",encoding="utf-8-sig")

if __name__ == '__main__':
    alldata()
# yahooplay()   
# outcome()