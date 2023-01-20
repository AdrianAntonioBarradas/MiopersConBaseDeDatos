from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta
import pytz
from unicodedata import normalize
import metrics as mt


MONGO_HOST = "132.247.22.53"
MONGO_PORT = 27017
MONGO_DB = "twitterdb"
MONGO_USER = "ConsultaTwitter"
MONGO_PASS = "$Con$ulT@C0V1D"

con = MongoClient(MONGO_HOST, MONGO_PORT)
db = con[MONGO_DB]
#db.authenticate(MONGO_USER, MONGO_PASS)

tz = pytz.timezone('America/Mexico_City')
today = datetime.now(tz=tz) #Obtenemos la fecha actual
today_minus = today - timedelta(days=1) # Quitamos un dia  de la fecha actual

timestamp = datetime.timestamp(today_minus) # Convertimos la fecha a timestamp


def convertDate(date):
    """
    El razonamiento en este método es que el locale del servidor de Miopers es actualmente es_mx, 
    mientras que el locale de la fecha del campo tweet['created_at'] es en_US.

    Refiérase a la documentación de Twiter:
    https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet#:~:text=Description-,created_at,-String

    Utilizamos diccionarios para convertir el locale de en_US a es_mx cuando sea necesario.

    Nota importante: este cambio se realiza porque el ambiente de CRON que ejecuta el job de master/src/main.py tiene locale es_mx.
    Cuando ejecutamos master/src/main.py desde bash, el locale es en_US.
    """
    
    format = '%a %b %d %H:%M:%S %z %Y'

    days = {
        'Mon': 'Lun', 'Tue': 'Mar', 'Wed': 'Mié', 'Thu': 'Jue', 'Fri': 'Vie', 'Sat': 'Sáb', 'Sun': 'Dom'
    }
    months = {
        'Jan': 'Ene', 'Feb': 'Feb', 'Mar': 'Mar', 'Apr': 'Abr', 'May': 'May', 'Jun': 'Jun', 
        'Jul': 'Jul', 'Aug': 'Ago', 'Sep': 'Sept', 'Oct': 'Oct', 'Nov': 'Nov', 'Dec': 'Dic'
    }
    
    try:
        result = datetime.strptime(date, format).astimezone(tz)
    except ValueError:
        date_list = date.split(' ')
    
        date_list[0] = days[date_list[0]]
        date_list[1] = months[date_list[1]]

        date = ' '.join(date_list)
        result = datetime.strptime(date, format).astimezone(tz)

    return result


def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('utf-8')


def downloadData(tweets,filtro):
    menciones = pd.DataFrame()
    hasht = pd.DataFrame()
    full_data = pd.DataFrame()
    for tweet in tweets:
        texto = tweet['text']
        try:
            texto = tweet['extended_tweet']['full_text']
        except:
            pass
        if mt.etiqueta_txt(texto, filtro) == 1:
            user = tweet['user']['screen_name']
            lugar = tweet['place']['full_name'].split(",")
            ubicacion = tweet['place']['full_name']
            id = tweet['id']
            fecha = convertDate(tweet['created_at'])
            if len(lugar) < 2:
                lugar.append('México')
            # mentions = tweet['entities']['user_mentions']
            # for xs in mentions:
            #     dic_menc = {'mencion': [xs['screen_name']], 'full_place': [ubicacion]}
            #     menciones = pd.concat([menciones, pd.DataFrame(dic_menc)], axis=0)
            # hashtags = tweet['entities']['hashtags']
            # for ys in hashtags:
            #     dic_hasht = {'hashtag': [ys['text']],  'full_place': [ubicacion]}
            #     hasht = pd.concat([hasht, pd.DataFrame(dic_hasht)], axis=0)
            trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
            texto = normalize('NFKC', normalize('NFKD', texto).translate(trans_tab))
            dataDic = {'usuario': [user], 'texto': [deEmojify(texto).replace('\n', ' ')],  'full_place': [ubicacion],'id':[id], 'fecha':[fecha]}
            data = pd.DataFrame(dataDic)
            full_data = pd.concat([full_data, data], axis=0)
    menciones = menciones.reset_index(drop=True)
    hasht = hasht.reset_index(drop=True)
    full_data = full_data.reset_index(drop=True)
    return (full_data, menciones, hasht)


def downloadData2(filtro):
    menciones = pd.DataFrame()
    hasht = pd.DataFrame()
    full_data = pd.DataFrame()
    cont = 0
    for tweet in db.tweetsMexico.find((({'$expr':{ '$gte':[  { '$toLong': "$timestamp_ms"},  1590440316.103616  ] }}))):
        if cont < 90000:
            cont = cont + 1
            texto = tweet['text']
            try:
                texto = tweet['extended_tweet']['full_text']
            except:
                pass
            if mt.etiqueta_txt(texto, filtro) == 1:
                user = tweet['user']['screen_name']
                lugar = tweet['place']['full_name'].split(",")
                ubicacion = tweet['place']['full_name']
                id = tweet['id']
                fecha = convertDate(tweet['created_at'])
                if len(lugar) < 2:
                    lugar.append('México')
                # mentions = tweet['entities']['user_mentions']
                # for xs in mentions:
                #     dic_menc = {'mencion': [xs['screen_name']], 'full_place': [ubicacion]}
                #     menciones = pd.concat([menciones, pd.DataFrame(dic_menc)], axis=0)
                # hashtags = tweet['entities']['hashtags']
                # for ys in hashtags:
                #     dic_hasht = {'hashtag': [ys['text']],  'full_place': [ubicacion]}
                #     hasht = pd.concat([hasht, pd.DataFrame(dic_hasht)], axis=0)
                trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
                texto = normalize('NFKC', normalize('NFKD', texto).translate(trans_tab))
                dataDic = {'usuario': [user], 'texto': [deEmojify(texto).replace('\n', ' ')], 'full_place': [ubicacion], 'id':[id], 'fecha':[fecha]}
                data = pd.DataFrame(dataDic)
                full_data = pd.concat([full_data, data], axis=0)
        else:
            menciones = menciones.reset_index(drop=True)
            hasht = hasht.reset_index(drop=True)
            full_data = full_data.reset_index(drop=True)
            return (full_data, menciones, hasht)
    menciones = menciones.reset_index(drop=True)
    hasht = hasht.reset_index(drop=True)
    full_data = full_data.reset_index(drop=True)
    return (full_data, menciones, hasht)
