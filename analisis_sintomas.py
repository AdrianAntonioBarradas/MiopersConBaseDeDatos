import metrics as mt
import downTweets as dt
import data_json as dj
from datetime import datetime
import pandas as pd

def ejecutarAnalisis(tweets, data_path):
    try: #importa los diccionarios
        filtro = mt.dataImport(['/home/adrian/Miopers/master/data/diccionarios/filtro_covid.txt'])
        sintomas = mt.dataImport([data_path+'diccionarios/sintomas.txt'])
        mentales = mt.dataImport([data_path+'diccionarios/mentales.txt'])
        direccion = data_path+'json/'
        mapa_alcaldias = direccion+'alcaldias.json'
        feed = data_path+"json/feed.pickle"
        feed_json = data_path+"json/feed.json"
    except :
        print("Error, Archivos no encontrados")
    today = datetime.now()
    dth = today.strftime('%a %b %d %H:%M:%S %Y')


    #try:
    #print(filtro, '\n',tweets[:10])
    dataFull = dt.downloadData(tweets,filtro)
    data = mt.ReturnDelegacion(dataFull[0])
    datam = mt.etiqueta(data, mentales)
    data_mp = datam[datam['etiqueta'] == 1]
    twe = data_mp['id'].tolist()
    data_p = mt.rept_clase(data_mp, 'mentales')
    data_f = mt.agrupaFecha(data_mp)

    dataS = mt.etiqueta(data, sintomas)
    data_Sp = dataS[dataS['etiqueta'] == 1]
    twe2 = data_Sp['id'].tolist()
    data_ps = mt.rept_clase(data_Sp, 'sintomas')
    data_f2 = mt.agrupaFecha(data_Sp)

    total = pd.merge(data_f, data_f2, on='fecha2')
    total.to_csv(data_path+'data_timeline.csv')
 
    dj.json_timeline(direccion+'timeline', total, dth) #esta función sobreescribe el JSON con la nueva info
    dj.procesar_mapa2(direccion+'alcaldias', mt.unionData(data_ps, data_p), mapa_alcaldias, dth)
    try:
        dj.list_id(twe+twe2, feed)
        dj.convert_pickle(feed, feed_json)
    except:
        print("Hubo algún error con el pickle")
    print('Analisis Sintomas terminado')
