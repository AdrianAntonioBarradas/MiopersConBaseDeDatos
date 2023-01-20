import matplotlib as plt
import numpy as np
import re
import pandas as pd

iterar = ['Ciudad de México', 'Campeche', 'Puebla', 'Estado de México',
          'Veracruz de Ignacio de la Llave', 'Hidalgo', 'Sinaloa',
          'Nuevo León', 'Quintana Roo', 'Jalisco', 'Coahuila de Zaragoza',
          'San Luis Potosí', 'Tamaulipas', 'Querétaro', 'Guanajuato',
          'Yucatán', 'Tabasco', 'Baja California', 'Oaxaca',
          'Sonora', 'Nayarit', 'Morelos', 'Durango',
          'Guerrero', 'Chihuahua', 'Michoacán de Ocampo', 'Chiapas',
          'Aguascalientes', 'Zacatecas', 'Tlaxcala', 'Baja California Sur',
          'Colima', 'Otro']

alcaldias = ['Álvaro Obregón', 'Azcapotzalco', 'Benito Juárez', 'Coyoacán',
             'Cuajimalpa', 'Cuauhtémoc', 'Gustavo A. Madero', 'Iztacalco',
             'Iztapalapa', 'Magdalena Contreras', 'Miguel Hidalgo', 'Milpa Alta',
             'Tláhuac', 'Tlalpan', 'Venustiano Carranza', 'Xochimilco']


'''
Funcion para obten de un txt texto y quitar emojis
return una lista de terminos o de textos
'''


def dataImport(filename):
    info = []
    for xs in filename:
        data = open(xs)
        for r in data:
            r = r.replace('\n', '')
            r = re.sub('https\W*t.co/\w*', '', r)
            info.append(r.encode('utf-8', 'ignore').decode('utf-8'))
    return info


'''
Funcion que etiqueta apartir de una lista de terminos
El dataFrame debe contener una columa de nombre texto
1 si el termino aparece 0 en otro caso
return un el dataFrame original con una columna etiqueta
'''


def etiqueta(data, etiqueta):
    data_text = data['texto'].tolist()
    list_et = []
    val = 0
    for xs in data_text:
        val = 0
        for ys in etiqueta:
            if len(re.findall(ys, xs.lower())) > 0:
                val = 1
                break
        list_et.append(val)
    eti_df = pd.DataFrame(list_et, columns=['etiqueta'])
    return pd.concat([data, eti_df], axis=1)


def etiqueta_txt(data, etiqueta):
    val = 0
    for ys in range(len(etiqueta)):
        if len(re.findall(etiqueta[ys], data.lower())) > 0:
            val = 1
            break
    return val


'''
Funcion que apartir de una lista de texto y una lista de terminos
saca el numero de apariciones de los terminos
return dataFrame con los terminos y su pertinente numero de apariciones
'''


def numApariciones(data, terminos):
    texto = data['texto'].tolist()
    numRepeticiones = []
    terminos_fil = []
    it = 0
    for xs in terminos:
        it = 0
        for ys in texto:
            it += len(re.findall(xs, ys.lower()))
        if it > 0:
            numRepeticiones.append(it)
            terminos_fil.append(xs)

    terminos_df = pd.DataFrame(terminos_fil, columns=['terminos'])
    aparaciones_df = pd.DataFrame(numRepeticiones, columns=['#Repeticiones'])
    return pd.concat([terminos_df, aparaciones_df], axis=1)


'''
Funcion que apartir de una lista de texto y una lista de terminos
saca el numero de apariciones de los terminos por estados de la republica
return dataFrame con los terminos y su pertinente numero de apariciones
'''


def numApariciones_eds(data, terminos, estado):
    info = []
    list_id = []
    texto = data['texto'].tolist()
    id_user = data['id'].tolist()
    numRepeticiones = []
    terminos_fil = []
    it = 0
    for xs in terminos:
        it = 0
        for ys in range(len(texto)):
            tam = len(re.findall(xs, texto[ys].lower()))
            if tam > 0:
                list_id.append(str(id_user[ys]))
            it += tam
        if it > 1:
            numRepeticiones.append(it)
            terminos_fil.append(xs)
    info.append([estado, terminos_fil, numRepeticiones])
    return [pd.DataFrame(info, columns=['Estado', 'terminos', '#Repeticiones']), list_id]
    # terminos_df = pd.DataFrame(terminos, columns=['terminos'])
    # aparaciones_df = pd.DataFrame(numRepeticiones, columns=['#Repeticiones'])
    # return pd.concat([terminos_df, aparaciones_df], axis=1)


'''
Funcion para hacer una  grafica de radar
apartir de un dataFrame con dos columna de nombre terminos y #Repeticiones
'''


def grafica_radar(data, termino):
    labels = np.array(data['terminos'])
    stats = data['#Repeticiones'].values

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    stats = np.concatenate((stats, [stats[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig = plt.figure(figsize=(22.2, 11.4))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2)
    ax.fill(angles, stats, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, labels)
    ax.set_title(termino + ' mas mencionados')
    ax.grid(True)
    plt.show()


def change_edo(data, archivo):
    estados = pd.read_csv(archivo, index_col=0)
    # Convertimos el dataset a diccionario donde la llave es el lugar
    estados = estados.drop_duplicates(subset='PlaceJson')
    estados = estados.set_index('PlaceJson').T.to_dict('list')
    ed_replace = []
    ed = data['full_place'].tolist()
    for xs in ed:
        try:
            if estados[xs] != 'nan':
                ed_replace.append(estados[xs][0])
            else:
                ed_replace.append('Otro')
        except:
            ed_replace.append('Otro')
    data = data.drop('full_place', axis=1)
    data['Estado'] = ed_replace
    return data


def ReturnDelegacion(df):
    dele = []
    newdf = pd.DataFrame()
    # newdf=pd.DataFrame(columns=['usuario', 'texto', 'full_place','delegacion'])
    for i in range(len(df)):
        if len(df['full_place'][i].split(", ")) == 2:
            if df['full_place'][i].split(", ")[1] == 'Distrito Federal':
                dele.append(df['full_place'][i].split(", ")[0])
                # print(df['full_place'][i].split(", ")[0])
                newdf.append(df.loc[[i]])
                newdf = newdf.append(df.iloc[[i]], ignore_index=True)
                # print(df.loc[[i]])
    newdf['delegacion'] = dele
    return newdf


def unionData(data1, data2):
    total = pd.DataFrame()
    lugar = data1['delegacion'].tolist()
    etiqueta = data1['clase'].tolist()
    numero = data1['total'].tolist()
    etiqueta1 = data2['clase'].tolist()
    numero1 = data2['total'].tolist()
    new_et = []
    new_numero = []
    for xs in range(len(etiqueta)):
        new_et.append(etiqueta[xs])
        new_et.append(etiqueta1[xs])
        new_numero.append(numero[xs])
        new_numero.append(numero1[xs])
        et = pd.DataFrame([[new_et]], columns=['clase'])
        num = pd.DataFrame([[new_numero]], columns=['total'])
        nomb = pd.DataFrame([lugar[xs]], columns=['delegacion'])
        pt = pd.concat([nomb, num, et], axis=1)
        total = pd.concat([total, pt], axis=0)
        new_et = []
        new_numero = []
    return total


def total_clase(data, alcaldia, clase):
    info = []
    num = len(data['etiqueta'].tolist())
    info.append([clase, alcaldia, num])
    return pd.DataFrame(info, columns=['clase', 'delegacion', 'total'])

# def total_clase_dia(data, alcaldia, clase):


def repetcions_ed(data, terminos):
    info_df = pd.DataFrame()
    list_id = []
    for xs in alcaldias:
        data_ed = data[data['delegacion'] == xs]
        info = numApariciones_eds(data_ed, terminos, xs)
        info_df = pd.concat([info_df, info[0]], axis=0)
        list_id = list_id + info[1]
    return [info_df, list_id]


def agrupaFecha(df):
    df.reset_index(inplace=True)
    fecha2 = []
    for i in range(len(df)):
        fq = df['fecha'][i]
        f_s = fq.strftime('%Y-%m-%d %H:%M:%S-05:00')
        fecha2.append(f_s.split(' ')[0])
    df['fecha2'] = fecha2
    a = df.groupby('fecha2').count().reset_index()
    a = a[['fecha2', 'etiqueta']]
    return a


def rept_clase(data, clase):
    info_df = pd.DataFrame()
    for xs in alcaldias:
        data_ed = data[data['delegacion'] == xs]
        info = total_clase(data_ed, xs, clase)
        info_df = pd.concat([info_df, info], axis=0)
    return info_df
