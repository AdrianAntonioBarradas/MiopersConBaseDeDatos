import json
import pandas as pd
import collections
import pickle
from IO_json import ordenar

def json_radar(nombre, data):
    f = open(nombre+".json", "w")
    lines = '[ \n'
    for indice_fila, fila in data.iterrows():
        lines += '{\n \"subject\": \"'+fila['terminos']+'\", \"A\":'+str(fila['#Repeticiones'])+'\n },\n'
    lines = lines[:len(lines)-2] + '\n]'
    f.write(lines)
    f.close()


def json_timeline(nombre, data, fecha):
    #cargar datos de la linea de tiempo
    with open("/home/adrian/Miopers/web/src/data/timeline.json", 'r') as json_file:
        timeline_dict = json.load(json_file)
    timeline_dict['time'] = fecha
    f = open(nombre+".json", "w")
    da = pd.read_csv('/home/adrian/Miopers/sintomas/data/data_timeline.csv')
    data = pd.concat([data, da], axis=0,sort=True)
    data = data.drop_duplicates(subset='fecha2', keep="last")
    lines = '{\n\"time\":\"' + fecha + '\",\n \"data\": [\n'
    
    for indice_fila, fila in data.iterrows():
        nueva_entrada = {}
        lines += '{ \"Sintomas mentales\":' + str(fila['etiqueta_x']) + ', \"Sintomas COVID\":'+ str(fila['etiqueta_y'])+', \"day\":\"'+ fila['fecha2']+'\"},\n'
        nueva_entrada['Sintomas mentales'] = fila['etiqueta_x']
        nueva_entrada['Sintomas COVID'] = fila['etiqueta_y']
        nueva_entrada['day'] = fila['fecha2']
        timeline_dict['data'].append(nueva_entrada)
    lines = lines[:len(lines)-2] + ']\n}'
    f.write(lines)
    f.close()
    
    #sobreescribir JSON local
    with open("/home/adrian/Miopers/web/src/data/timeline.json", 'w') as json_file:
        json.dump(ordenar(timeline_dict), json_file)
    #subir JSON al repo
    #IO_json.upload_json("sintomas/data/json/timeline.json",timeline_dict)


def json_tm(nombre, datas, archivo):
    fecha = datas['fecha2'].tolist()
    mentales = datas['etiqueta_x'].tolist()
    sintomas = datas['etiqueta_y'].tolist()
    with open(archivo, encoding='utf-8') as feedsjson:
        da = json.load(feedsjson)
        p = da['data']
        for xs in range(len(fecha)):
            entry = {'Sintomas mentales': mentales[xs], 'Sintomas COVID': sintomas[xs], 'day': fecha[xs]}
            p.append(entry, ignore_index=True)
    json.dump(da)


def mod(nombre, archivo):
    with open('/home/adrian/Miopers/sintomas/data/json/alcaldias.json') as file:
        info = json.load(file)
        for xs in info['features']:
            pro = xs['properties']
            pro['data'] = {}
        print(info)
        with open(nombre + '.json', 'w') as file:
            json.dump(info, file, indent=4)


def json_alcaldias(nombre, data, archivo, fecha):
    lugar = data[0]
    etiqueta = data[1]
    numero = data[2]
    with open(archivo) as file:
        info = json.load(file)
        info['time'] = fecha
        for xs in info['features']:
            pro = xs['properties']
            data = pro['data']
            for ys in range(len(lugar)-1):
                lu = lugar[ys]
                if lu == 'Cuajimalpa':
                    lu = 'Cuajimalpa de Morelos'
                elif lu == 'Magdalena Contreras':
                    lu = 'La Magdalena Contreras'
                elif lu == 'Xochimilco':
                    lu = 'Xochimilco'
                if pro['nomgeo'] == lu:
                    et = etiqueta[ys]
                    num = numero[ys]
                    for ds in range(len(et)):
                        data[et[ds]] = num[ds]
        with open(nombre + '.json', 'w') as file:
            json.dump(info, file, indent=4)
    #sobreescribir JSON local
    with open("/home/adrian/Miopers/web/src/data/alcaldias_result.json",'w') as json_file:
        json.dump(info,json_file)
    #subir JSON al repo Miopers
    #IO_json.upload_heavy("sintomas/data/json/alcaldias_result.json", info,"Actualizar JSON")


def json_mapa(nombre, data, archivo):
    lugar = data[0]
    etiqueta = data[1]
    numero = data[2]
    with open(archivo) as file:
        data = json.load(file)
        for xs in data['features']:
            pro = xs['properties']
            for ys in range(len(lugar)-1):
                lu = lugar[ys]
                if lu == 'Cuajimalpa':
                    lu = 'Cuajimalpa de Morelos'
                elif lu == 'Magdalena Contreras':
                    lu = 'La Magdalena Contreras'
                elif lu == 'Xochimilco':
                    lu = 'Xochimilco'
                if pro['name'] == lu:
                    et = etiqueta[ys]
                    num = numero[ys]
                    for ds in range(len(et)-1):
                        pro[et[ds]] = num[ds]
        with open(nombre + '.json', 'w') as file:
            json.dump(data, file, indent=4)
        


def procesar_mapa(nombre, data, archivo):
    lugar = data['Estado'].tolist()
    etiqueta = data['Hashtag'].tolist()
    numero = data['Num_Hash'].tolist()
    json_mapa(nombre[0], [lugar, etiqueta, numero], archivo)
    lugar = data['Estado'].tolist()
    etiqueta = data['Mencion'].tolist()
    numero = data['Num_mencion'].tolist()
    json_mapa(nombre[1], [lugar, etiqueta, numero], archivo)
    lugar = data['Estado'].tolist()
    etiqueta = data['Usuario_Activo'].tolist()
    numero = data['Num_Usr'].tolist()
    json_mapa(nombre[2], [lugar, etiqueta, numero], archivo)


def list_id(data, archivo):
    rept = [x for x, y in collections.Counter(data).items() if y > 1]
    with open(archivo, "wb") as f:
        pickle.dump(rept, f)


def convert_pickle(pickle, path_json):
    feed = pd.read_pickle(pickle)  # cambiar la ruta del pickle
    with open(path_json, 'w') as f:
        f.write('[')
        for i in feed[:-2]:
            f.write('"'+str(i)+'"'+',')
        f.write('"'+str(feed[-1])+'"'+']')


def procesar_mapa2(nombre, data, archivo, fecha):
    lugar = data['delegacion'].tolist()
    etiqueta = data['clase'].tolist()
    numero = data['total'].tolist()
    json_alcaldias(nombre, [lugar, etiqueta, numero], archivo, fecha)
