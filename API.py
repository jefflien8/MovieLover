import datetime
import requests
from flask import *
from flask_cors import CORS
import pymysql
from pymysql import NULL
# from dbutils.pooled_db import PooledDB, SharedDBConnection
# import pymysql.cursors

apiBlueprint=Blueprint("api",__name__)
CORS(apiBlueprint)
db=pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    database='movielover', 
    charset='utf8'
)
# pool = PooledDB(
#     creator=pymysql,
#     maxconnections=6,
#     mincached=2,
#     maxcached=5,
#     maxshared=3,
#     blocking=True,
#     maxusage=None,
#     setsession=[],
#     ping=0,
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='123456',
#     database='website', 
#     charset='utf8',
#     Cursor=pymysql.cursors.DictCursor
# )
# conn = pool.connection()

cursor=db.cursor()

@apiBlueprint.route("/api/movies")
def API():
    page=request.args.get("page",0, type=int)
    keyword=request.args.get("keyword", None,type=str)
    if keyword ==None:
        sql='''SELECT * FROM `movies` ORDER BY `poster_url` LIMIT %s,%s'''
        cursor.execute(sql,(page*12,12))
        result=cursor.fetchall()
        cursor.execute(sql,((page+1)*12,12))
        resultNext=cursor.fetchall()
        cursor.close
        resultNextLen=len(resultNext)
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
    cursor.execute(sql,(movieId))
    result = cursor.fetchone()
    cursor.close
    if result == None:
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
