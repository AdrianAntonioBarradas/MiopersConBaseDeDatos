# encoding:utf8
from pymongo import MongoClient
from datetime import datetime, timedelta, date
import time
import json
import re
import urllib
from IO_json import ordenar

#mongo --host 132.247.22.53:27017 -u ConsultaTwitter --authenticationMechanism SCRAM-SHA-256 --authenticationDatabase twitterdb


'''
Palabras de contexto

Se busca
- Comportamiento del usuario
- Estado de animo
- Medidas del gobierno
- Síntomas del usuario


Para obtener contexto sacaré 2 palabras principales de 3 categorías:
1.- Hashtags
2.- Personas (Menciones)
3.- Sintomas
Con sus diferentes variaciones


1.-
- (covid19) covid covidmx
- (coronavirus) virus
- quedateencasa cuarentena encasa
2.-
- (Gatell)
- (AMLO) andres manuel lopez obrador
- SusanaDistancia
3.-
- (ansiedad)
- (depresión)
'''

def getText(tweet):
    """
    Summary: Función que permite extraer la información de los tweets descargados desde Monto para ser procesados.
        Los textos de los tweets pueden ser descargados de forma total, truncada o el texto completo, dependiendo de
        la calidad del tweet descargado. 
    Args:
        tweet: Variable para identificar el texto de cada uno de los tweets descargados

    Returns:
        list: Se devuelve una lista con la información del texto de todos los tweets, estos pueden ser
        de forma total o de forma parcial, dependiendo de la condición del tweet

    """
    return tweet['text'] if not tweet['truncated'] else tweet['extended_tweet']['full_text']

def getDate(tweet):
    """
    Summary: Función para poder extraer de los tweets la fecha de cuando fueron emitidos cada uno de estos.
    
    Args:
        tweet: Variable para identificar el texto de cada uno de los tweets descargados

    Returns:
        Se devuelve la fecha de publicación de cada uno de los tweets en formato datetime. 

    """
    timestamp = tweet['timestamp_ms'][:-3]
    return datetime.fromtimestamp(int(timestamp)) + timedelta(hours=5)

def ejecutarAnalisis(tweets, data_path):    
    # Creamos una expresión regular para volver a extraer, aquellos tweets que tienen información relevante. 
    contexto = re.compile(r'(covid|(v|b)iru(s|z)|sars(-| )?cov|contingencia|sanitaria|sintoma|neumonia|quedateencasa|pandemia|encierro|cuarentena|encasa|cuandoestoseacabe|aislamientosocial|susana ?distancia)',re.I)

    # Creamos un diccionario para poder guardar la información de los hashtags
    timeline = dict()
    # Información de las palabras claves y hastags relevantes para el estudio.  
    tokens = ['quedateencasa','coronavirus', 'covid19' ,'@HLGatell','@lopezobrador_','SusanaDistancia']

    # Inicialización del tiempo de ejecución del script
    start_time = time.time()

    # Variable para poder contar el número de veces que aparece alguno de los topicos de interés en los tweets
    total_contexto = 0

    # Buscamos entre los tweets consultados de Mongo
    for i,tweet in enumerate(tweets):
        # Extraemos tweets, la fecha en que se emitieron y los almacenamos en variables
        text = getText(tweet)
        date = getDate(tweet).date()
        data = timeline.get(str(date),{})
        #print('Fecha: ' + str(getDate(tweet)))


        # Vamos analizando cada uno de los tweets y contabilizamos el número de estos. 
        total_contexto = total_contexto + 1
        # Buscamos cada uno de los tokens y si los hayamos en una lista guardamos un registro de ellos y aumentamos el contador
        for token in tokens:
            if token in text:
                aux = data.get(token,0)
                data[token] = aux + 1
            else:
                data[token] = data.get(token,0)


        timeline[str(date)] = data

    #descargamos un diccionario con la info historica
    with open("/home/adrian/Miopers/web/src/data/datatimeline_result.json", "r") as json_file:
        results = json.load(json_file)
    
    # Creamos una nueva lista para almacenar la información de las fechas de los tweets
    data = list()
    for d in sorted(timeline.keys()):
        # Vamos recorreiendo el diccionario creado con anterioridad y vemos la fecha de su creaación y los enumeramos
        aux = timeline.get(d,{})
        aux['day'] = d
        data.append(aux)
        results['data'].append(aux) #actualizar el diccionario con la info historica

    # Creamos un diccionario final para ir almacenando toda la información final.
    #results = dict()
    
    
    # Guardamos en el diccionario la información de cuando fue procesado el script.
    results['time'] = datetime.today().ctime()

    # Creamos un archivo .json donde guardamos la información de lo anteriormente procesado para su posterior uso. 
    print( results)
    print("peopoepeopeoe")
    with open("/home/adrian/Miopers/web/src/data/timeline_result.json", "w") as json_file:
        json.dump(ordenar(results), json_file)
    #subir JSON al repositorio miopers
    #import IO_json
    #IO_json.upload_json("home/data/timeline_result.json",results)
    
    print("home: linea de tiempo actualizada\n--- %s segundos ---" % (time.time() - start_time))
    
    return json_file
