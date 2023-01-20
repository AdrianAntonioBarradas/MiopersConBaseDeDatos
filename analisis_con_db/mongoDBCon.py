from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime, timedelta
from typing import List
import pandas as pd
import re
from functools import reduce


#Establecimiento de Parámetros
MONGO_DB = 'twitterdb'
MONGO_HOST = '132.247.22.53'
MONGO_USER = 'ConsultaTwitter'
MONGO_PASS = '$Con$ulT@C0V1D'
MONGO_MECHANISM = 'SCRAM-SHA-25'

#Línea de Conexión Productiva
uri = f'mongodb://{quote_plus(MONGO_USER)}:{quote_plus(MONGO_PASS)}@{MONGO_HOST}/{MONGO_DB}'

client3 = MongoClient(uri)
db3 = client3.twitterdb
collection = db3.tweetsMexico


def fechas_milisegundos(fecha_inicial, fecha_final):
    """recibe fechas en formato YYYY-mm-dd y las regresa en milisegundos, la fecha final la regresa a las 0:00 horas i.e. es al comienzo del dia"""
    formato_fecha = "%Y-%m-%d"
    fechaInicial = datetime.strptime(fecha_inicial, formato_fecha)
    #milliseconds1 = int(round(fechaInicial.timestamp() * 1000))-18000000 #se restan los milisegundos a 5 horas para coincidir con la zona horaria que traen los tweets 
    milliseconds1 = int(round(fechaInicial.timestamp() * 1000))#- 21600000 #se restan los milisegundos a 6 horas para coincidir con la zona horaria que traen los tweets 
    
    fechaFinal = datetime.strptime(fecha_final, formato_fecha)
    #milliseconds2 = int(round(fechaFinal.timestamp() * 1000))-18000000
    milliseconds2 = int(round(fechaFinal.timestamp() * 1000))#-21600000
    return milliseconds1,milliseconds2  

def dataImport(diccWords) -> List[str]:
    """lee una lista de palabras, cada renglón es un elemento de la lista resultante"""
    tokens = []
    for word in diccWords.split('\n'):
        tokens.append(word)
    return tokens

def crearExpresion(terminos):
    """recibe una lista de terminos, los concatena con | para crear  una regex"""
    def concatenarOR(elemento1, elemento2):
        """Recibe dos strings, las concatena separándolas con símbolo |"""
        return elemento1+"|"+elemento2
    return reduce(concatenarOR,terminos)

#para fechas especificas
def consulta(fecha_inicial, fecha_final, db):
    """obtiene todos los tweets relacionados al coronavirus dentro de las fechas especificadas. Regresa una lista de documentos (diccionarios)."""
    sql = "SELECT diccionario_tema FROM temas  WHERE tema LIKE 'COVID';"
    ndic = db.selectOne(sql) #para modificar cuando se convierta a class
    expresion = crearExpresion(dataImport(ndic))
    regex = re.compile(expresion, re.I)
    tiempo1, tiempo2 = fechas_milisegundos(fecha_inicial, fecha_final)
    pipeline = [
        {
            '$match': {
                '$and': [
                    {
                        'timestamp_ms': {
                            '$gte': str(tiempo1)
                        }
                    }, 
                    {
                        'timestamp_ms': {
                            '$lt': str(tiempo2)
                        }
                    }
                ]
            }
        },
        {
            '$match': {
                '$or': [
                    {
                        'truncated': False,
                        'text': {
                            '$regex': regex
                        }
                    },
                    {
                        'truncated': True,
                        'extended_tweet.full_text': {
                            '$regex': regex
                        }
                    }
                ]
            }
        }
    ]
    cursor = collection.aggregate(pipeline)
    return list(cursor)

def consulta_sin_filtro(fecha_inicial, fecha_final):
    """obtiene todos los tweets contenidos en el servidor de Miopers en las fechas especificadas. Regresa una lista de documentos (diccionarios)"""
    tiempo1, tiempo2 = fechas_milisegundos(fecha_inicial, fecha_final)
    myquery = {'$expr':{'$and':[
            { '$gte':[  { '$toLong': "$timestamp_ms"}, tiempo1 ]},
            { '$lt':[  { '$toLong': "$timestamp_ms"}, tiempo2 ]}]}
               }
    #proyeccion = ['text'] #de cada documento solo descargamos los campos que nos interesan
    #cursor = collection.find(filter=myquery, projection=proyeccion)
    cursor = collection.find(filter=myquery)
    tweets = list(cursor)
    return tweets


def fechas_ayer_hoy_string():
    """Obtener la fecha de ayer y hoy en formato YYYY-mm-dd (con 0:00 horas)"""
    hoy = datetime.now()
    hoy_str = hoy.strftime("%Y-%m-%d")
    ayer = datetime.strptime(hoy_str, "%Y-%m-%d") - timedelta(days=1)
    ayer_str = ayer.strftime("%Y-%m-%d")
    return ayer_str, hoy_str

    
def consulta_ayer(db):
    """Descarga los tweets del día anterior (ya filtrados)"""
    #obtener fecha de ayer y hoy en formato dd-mm-YYYY
    ayer_str, hoy_str = fechas_ayer_hoy_string()
    
    return consulta(ayer_str, hoy_str, db)