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

    con1=engine.connect()
    cursor =con1.execute(sql,(movieId))
    result=cursor.fetchone()
    con1.close()

    if result == []:
        return {"error": True,"message": "無此編號"}
    elif result != []:
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
    con1 = engine.connect()
    cursor = con1.execute(sql,(movieId))
    result = cursor.fetchone()
    con1.close()
    data=[]

    if result == []:
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

@apiBlueprint.route("/session", methods=["GET"])
def getSession():
    if request.method == 'GET':
        print(session.get("name"))
        return jsonify({"name": session.get("name"),"email": session.get("email")})

@apiBlueprint.route("/api/member", methods=["POST"])
def signup():
    data=request.get_json()
    newname=data["name"]
    newemail=data["email"]
    newpassword=data["password"]

    if (newname=="")|(newemail=="")|(newpassword==""):
        return jsonify({"error": True,"message": "請填寫完整"})

    sql = '''SELECT `email` FROM `member` WHERE `email`=%s'''
    con1 = engine.connect()
    cursor = con1.execute(sql,(newemail))
    result = cursor.fetchone()

    if(result != None):
        return jsonify({"error": True,"message": "Email已經被註冊"})
        
    elif(result == None):
        sql='''INSERT INTO `member`(name,email,password) VALUE(%s,%s,%s)'''
        try:
            cursor = con1.execute(sql,(newname,newemail,newpassword))
            # engine.commit()
        except:
            # engine.rollback()
            print('error')
        con1.close()
        
        return jsonify({"ok": True})
    else:
        return jsonify({"error": True,"message": "伺服器錯誤，請稍後再試"})

@apiBlueprint.route("/api/member", methods=["GET"])
def getStatue():
    print(session["name"])
    if (session["name"] == None):
        return jsonify({"data":None})
    else:
        data={
            "data": {
                "id": session["id"],
                "name": session["name"],
                "email": session["email"]
                }
        }
        return jsonify(data)

@apiBlueprint.route("/api/member", methods=["PATCH"])
def login():
    data=request.get_json()
    email=data["email"]
    password=data["password"]

    sql='''SELECT `member_id`,`name`,`email` FROM `member` WHERE `email`=%s AND `password`=%s'''
    con1 = engine.connect()
    cursor = con1.execute(sql,(email,password))
    result = cursor.fetchone()

    if(result != []):
        session["id"] = result[0]
        session["name"] = result[1]
        session["email"] = result[2]
        session.permanent=True
        return jsonify({"ok": True})

    elif(result == []):
        return jsonify({"error": True,"message": "帳號或密碼錯誤"})
    else:
        return jsonify({"error": True,"message": "伺服器錯誤，請稍後再試"})

@apiBlueprint.route("/api/member", methods=["DELETE"])
def signout():
    session["id"] = None
    session["name"] = None
    session["email"] = None
    print(session["name"])
    return jsonify({"ok": True})

@apiBlueprint.route("/api/favorite", methods=["POST"])
def addFavorite():
    data = request.get_json()
    movie_name_ZH = data["movie_name_ZH"]
    movie_name_EN = data["movie_name_EN"]
    poster_url = data['poster_url']
   
    if (movie_name_ZH == "")|(movie_name_EN == ""):
        return jsonify({"error": True,"message": "收藏失敗"})

    sql = '''SELECT `fav_index` FROM `favorite` WHERE `movie_name_ZH`= %s AND `member_id`= %s'''
    con1 = engine.connect()
    cursor = con1.execute(sql,(movie_name_ZH,session['id']))
    result = cursor.fetchone()
    print(result)
    if(result != None):
        return jsonify({"error": True,"message": "已經在收藏內"})
        
    elif(result == None):
        sql='''INSERT INTO `favorite`(member_id,movie_name_ZH,movie_name_EN,poster_url) VALUE(%s,%s,%s,%s)'''
        try:
            cursor = con1.execute(sql,(session['id'],movie_name_ZH,movie_name_EN,poster_url))
            # engine.commit()
        except:
            # engine.rollback()
            print('error')
        con1.close()
        
        return jsonify({"ok": True})
    else:
        return jsonify({"error": True,"message": "伺服器錯誤，請稍後再試"})

@apiBlueprint.route("/api/favorite", methods=["GET"])
def GETfavorite():
    if (session["name"] == None):
        return jsonify({"data":None})
    else:
        sql = '''SELECT * FROM `favorite` WHERE `member_id`= %s'''
        con1 = engine.connect()
        cursor = con1.execute(sql,(session['id']))
        result = cursor.fetchall()

        data = []
        for i in result:
            sql = '''SELECT * FROM `movies` WHERE `movie_name_ZH`= %s'''
            cursor = con1.execute(sql,(i[2]))
            favResult = cursor.fetchone()
            print(favResult)
            if favResult != None:
                data.append({
                    "index":favResult[0],
                    "movie_name_ZH":favResult[1],
                    "movie_name_EN":favResult[2],
                    "yahoo_id":favResult[3],
                    "ambassador_id":favResult[4],
                    "showtime_id":favResult[5],
                    "poster_url":favResult[6],
                    "release_date":favResult[7],
                    'movie_info':favResult[8],
                    'fav_index':i[0]
                })
            else:
                data.append({
                    'fav_index':i[0],
                    'movie_name_ZH':i[2],
                    'movie_name_EN':i[3],
                    'poster_url':i[4]
                })
            
        datas={'data':data} 
        # print(datas)
        return jsonify(datas)

@apiBlueprint.route("/api/favorite", methods=["DELETE"])
def DELfavorite():
    data = request.get_json()
    fav_index = data["fav_index"]

    sql = '''SELECT * FROM `favorite` WHERE `fav_index`= %s'''
    con1 = engine.connect()
    cursor = con1.execute(sql,(fav_index))
    result = cursor.fetchone()

    if result != None:
        sql = '''DELETE FROM `favorite` WHERE `fav_index`=%s'''
        con1.execute(sql,(fav_index))
        return jsonify({"ok": True})
    else:
        return jsonify({"error": True,"message": "無此收藏"})
   