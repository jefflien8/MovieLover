import datetime
from h11 import Data
import requests
from flask import *
from flask_cors import CORS
import pymysql
from pymysql import NULL
from sqlalchemy import create_engine
# import pymysqlpool
# from pymysqlpool import Pool
import pymysql.cursors

apiBlueprint=Blueprint("api",__name__)
CORS(apiBlueprint)
# db=pymysql.connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='123456',
#     database='movielover', 
#     charset='utf8'
# )
# pymysqlpool.logger.setLevel('DEBUG')
engine = create_engine('mysql+pymysql://root:12345678@localhost/movielover', pool_size=20, max_overflow=0)

# pool = Pool(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='123456',
#     database='movielover', 
#     charset='utf8' )
# pool.init()
# config={'host':'localhost', 'user':'root', 'password':'12345678', 'database':'movielover', 'autocommit':True}
# pool1 = pymysqlpool.ConnectionPool(size=2, maxsize=3, pre_create_num=2, name='pool1', **config)


@apiBlueprint.route("/api/movies")
def API():

    page=request.args.get("page",0, type=int)
    keyword=request.args.get("keyword", None,type=str)
    if keyword == None:
        sql='''SELECT * FROM `movies` ORDER BY `data_id` LIMIT %s,%s'''

        # con1 = pool.get_connection()
        # with con1 as connection:
        #     with connection.cursor() as cursor:
        #         cursor.execute(sql,(page*12,12))
        #         result=cursor.fetchall()
        #         cursor.execute(sql,((page+1)*12,12))
        #         resultNext=cursor.fetchall()
        #         cursor.close()
        con1=engine.connect()
        rows =con1.execute(sql,(page*12,12))
        result=rows.fetchall()
        row2 =con1.execute(sql,((page+1)*12,12))
        resultNext=row2.fetchall()
        con1.close()
        resultNextLen=len(resultNext)
        print(result)
        data=[]
        for i in result:
            data.append({
                "data_id":i[0],
                "movie_name_ZH":i[1],
                "movie_name_EN":i[2],
                "yahoo_id":i[3],
                "ambassador_id":i[4],
                "showtime_id":i[5],
                "poster_url":i[6],
                "release_date":i[7],
            })
        if resultNextLen==0:
            nextPage=None
            AllData={"nextPage":nextPage,
                "data":data
            }
            return jsonify(AllData)
        else:
            AllData={"nextPage":page+1,
                "data":data
            }
            return jsonify(AllData)

    # elif keyword!=None:
    #     sql='''SELECT `id`,`name`,`category`,`description`,`address`,`transport`,
    #     `mrt`,`latitude`,`longitude`,`images`FROM `spot` WHERE `name` LIKE %s ORDER BY `id` LIMIT %s,%s'''
    #     cursor.execute(sql,("%"+keyword+"%",page*12,12))
    #     seachResult=cursor.fetchall()
    #     cursor.execute(sql,("%"+keyword+"%",(page+1)*12,12))
    #     seachResultNext=cursor.fetchall()
    #     cursor.close
    #     seachResultNextLen=len(seachResultNext)
    #     sreachData=[]
    #     for j in seachResult:
    #         urlsql='''SELECT`url` FROM `url` WHERE `url_id`= %s'''
    #         cursor.execute(urlsql,(j[0]))
    #         urlResult=cursor.fetchall()
    #         cursor.close
    #         url=[url[0] for url in urlResult]
    #         sreachData.append({
    #             "id":j[0],
    #             "name":j[1],
    #             "category":j[2],
    #             "description":j[3],
    #             "address":j[4],
    #             "transport":j[5],
    #             "mrt":j[6],
    #             "latitude":j[7],
    #             "longitude":j[8],
    #             "images":url
    #             })
    #     if seachResultNextLen == 0:
    #         nextPage=None
    #         resultData={"nextPage":nextPage,
    #             "data":sreachData
    #         }
    #         return jsonify(resultData)
    #     else: 
    #         resultData={"nextPage":page+1,
    #         "data":sreachData
    #         }
    #         return jsonify(resultData)

    else:
        return {"error": True,"message": "伺服器錯誤，請稍後再試"}

@apiBlueprint.route("/api/movie/<movieId>")
def movieAPI(movieId):
    sql = '''SELECT * FROM `movies` WHERE `data_id`=%s'''
    # con1 = pool.get_connection()
    # with con1 as connection:
    #     with connection.cursor() as cursor:
    #         cursor.execute(sql,(movieId))
    #         result = cursor.fetchone()
    #         cursor.close()
    con1=engine.connect()
    cursor =con1.execute(sql,(movieId))
    result=cursor.fetchone()
    print(result)
    if result == []:
        return {"error": True,"message": "無此編號"}
    elif result!= None:
        Data={
            "data": {
                "data_id":result[0],
                "movie_name_ZH":result[1],
                "movie_name_EN":result[2],
                "yahoo_id":result[3],
                "ambassador_id":result[4],
                "showtime_id":result[5],
                "poster_url":result[6],
                "release_date":result[7],
            }
        }      
        return jsonify(Data)
    else:
        return {"error": True,"message": "伺服器錯誤，請稍後再試"}

@apiBlueprint.route("/api/movieScreening/<movieId>")
def movieScreening(movieId):
    sql = '''SELECT `movie_name_ZH` FROM `movies` WHERE `data_id`=%s'''
    # con1 = pool.get_connection()
    # with con1 as connection:
    #     with connection.cursor() as cursor:
    #         cursor.execute(sql,(movieId))
    #         result = cursor.fetchone()
    #         cursor.close()
    con1=engine.connect()
    cursor =con1.execute(sql,(movieId))
    result=cursor.fetchall()
    data=[]
    
    if result == []:
        return {"error": True,"message": "無此編號"}

    elif result!= None:    
        sql = '''SELECT * FROM `yahooscreenings` WHERE `movie_name_ZH`=%s'''
        # con1 = pool1.get_connection()
        # with con1 as connection:
        #     with connection.cursor() as cursor:
        #         cursor.execute(sql,(result))
        #         Screening = cursor.fetchone()
        #         Screenings = cursor.fetchall()
        #         cursor.close()
        con1=engine.connect()
        cursor =con1.execute(sql,(result))
        Screenings = cursor.fetchall()
        Screening = cursor.fetchone()
        print(Screenings)

        if Screenings == []:
            return {"error": True,"message": "查無場次"}

        for i in Screenings:
            data.append({
                "data_id":i[0],
                "movie_name_ZH":i[1],
                "theater":i[2],
                "date":i[3],
                "time":i[4],
                "type":i[5],
            })     
        datas={'data':data} 
        return jsonify(datas)
    
    else:
        return {"error": True,"message": "伺服器錯誤，請稍後再試"}