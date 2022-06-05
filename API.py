# from google.oauth2 import id_token
# from google.auth.transport import requests

from flask import *
from flask_cors import CORS
import pymysql
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
        sql='''SELECT * FROM `movies` ORDER BY `index` LIMIT %s,%s'''

        # con1 = pool.get_connection()
        # with con1 as connection:
        #     with connection.cursor() as cursor:
        #         cursor.execute(sql,(page*12,12))
        #         result=cursor.fetchall()
        #         cursor.execute(sql,((page+1)*12,12))
        #         resultNext=cursor.fetchall()
        #         cursor.close()
        con1 = engine.connect()
        rows = con1.execute(sql,(page*12,12))
        result = rows.fetchall()
        row2 = con1.execute(sql,((page+1)*12,12))
        resultNext = row2.fetchall()
        con1.close()
        resultNextLen=len(resultNext)
   
        data=[]
        for i in result:
            data.append({
                "index":i[0],
                "movie_name_ZH":i[1],
                "movie_name_EN":i[2],
                "yahoo_id":i[3],
                "ambassador_id":i[4],
                "showtime_id":i[5],
                "poster_url":i[6],
                "release_date":i[7],
                'movie_info':i[8]
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

    elif keyword!=None:
        sql='''SELECT * FROM `movies` WHERE `movie_name_ZH` LIKE %s OR `movie_name_EN` LIKE %s ORDER BY `index`'''
        con1 = engine.connect()
        cursor=con1.execute(sql,("%"+keyword+"%","%"+keyword+"%"))
        result=cursor.fetchall()
        con1.close

        sreachData=[]
        for i in result:
            sreachData.append({
                "index":i[0],
                "movie_name_ZH":i[1],
                "movie_name_EN":i[2],
                "yahoo_id":i[3],
                "ambassador_id":i[4],
                "showtime_id":i[5],
                "poster_url":i[6],
                "release_date":i[7],
                'movie_info':i[8]
            })
        resultData={
            "data":sreachData
        }        
        if result == []: 
            resultData={
            "data":None
            }
            return jsonify(resultData)
        else:
            return jsonify(resultData)



    else:
        return {"error": True,"message": "伺服器錯誤，請稍後再試"}

@apiBlueprint.route("/api/movie/<movieId>")
def movieAPI(movieId):
    sql = '''SELECT * FROM `movies` WHERE `index`=%s'''
    # con1 = pool.get_connection()
    # with con1 as connection:
    #     with connection.cursor() as cursor:
    #         cursor.execute(sql,(movieId))
    #         result = cursor.fetchone()
    #         cursor.close()
    con1=engine.connect()
    cursor =con1.execute(sql,(movieId))
    result=cursor.fetchone()
    
    if result == []:
        return {"error": True,"message": "無此編號"}
    elif result!= None:
        Data={
            "data": {
                "index":result[0],
                "movie_name_ZH":result[1],
                "movie_name_EN":result[2],
                "yahoo_id":result[3],
                "ambassador_id":result[4],
                "showtime_id":result[5],
                "poster_url":result[6],
                "release_date":result[7],
                "movie_info":result[8]
            }
        }      
        return jsonify(Data)
    else:
        return {"error": True,"message": "伺服器錯誤，請稍後再試"}

@apiBlueprint.route("/api/movieScreening/<movieId>")
def movieScreening(movieId):
    time = request.args.get("time",None,type=str)
    date = request.args.get("date",None, type=str)
    sql = '''SELECT `yahoo_id` FROM `movies` WHERE `index`=%s'''
    con1=engine.connect()
    cursor =con1.execute(sql,(movieId))
    result=cursor.fetchone()
    data=[]

    if result == None:
        return {"error": True,"message": "無此編號"}

    elif result!= None:   
        if date:
            sql = '''SELECT * FROM `yahooscreenings` WHERE `yahoo_id`=%s AND `date`=%s ORDER BY `yahoo_index`'''
        if date and time:
            sql = '''SELECT * FROM `yahooscreenings` WHERE `yahoo_id`=%s AND `date`=%s ORDER BY `time`'''
        # else: 
        #     sql = '''SELECT * FROM `yahooscreenings` WHERE `yahoo_id`=%s'''    
        con1=engine.connect()
        cursor =con1.execute(sql,(result[0],date))
        Screenings = cursor.fetchall()

        if Screenings == []:
            return {"error": True,"message": "無上映場次"}

        for i in Screenings:
            data.append({
                "index":i[0],
                "yahoo_id":i[1],
                "theater":i[2],
                "date":i[3],
                "time":i[4],
                "type":i[5],
            })     
        datas={'data':data} 
        return jsonify(datas)
  
            # con1=engine.connect()
            # cursor =con1.execute(sql,(result))
            # Screenings = cursor.fetchall()

            # if Screenings == []:
            #     return {"error": True,"message": "查無場次"}

            # for i in Screenings:
            #     data.append({
            #         "index":i[0],
            #         "yahoo_id":i[1],
            #         "theater":i[2],
            #         "date":i[3],
            #         "time":i[4],
            #         "type":i[5],
            #     })     
            # datas={'data':data} 
            # return jsonify(datas)
    
    else:
        return {"error": True,"message": "伺服器錯誤，請稍後再試"}

# @apiBlueprint.route("/api/member")
# def movieScreening():


