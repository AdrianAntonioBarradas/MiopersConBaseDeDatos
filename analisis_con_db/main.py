#!/usr/bin/env python3
#!/usr/bin/env bash
DISPLAY=':0.0'

from DataBaseCon import DataBase
import mongoDBCon

db = DataBase()
#descargar tweets (ya filtrados)
print("Descargando tweets...")
#tweets = mongo.consulta_ayer()

tweets =  mongoDBCon.consulta_ayer(db)
print("finish")

def insertProcesoTweets (db):
        #crear regsitro de proceso en la base de datos
    id_tema = 1 #corresponde al tema: COVID
    #tanto el id_proceso y fecha_inicio se generan automáticamente al realizar el insert
    sql = "INSERT INTO proceso (id_tema, conteo_tweet) VALUES ({}, {});".format(id_tema, len(tweets))
    print(sql)
    #db.update(sql)
    sql = "SELECT max(id_proceso) from proceso;"
    currentProcess = db.selectOne(sql)
    print("El id de proceso es : ", currentProcess)
    def getId (tweets):
        return tweets['id']
    sql = "INSERT INTO tweet (id_proceso, id_tweet) VALUES "
    for  i in tweets:
        comp = "({},'{}'),".format(currentProcess, getId(i))
        sql = sql + comp
        
    sql = sql[: -1]
    sql = sql + ";"

    print(sql)
    #db.update(sql)