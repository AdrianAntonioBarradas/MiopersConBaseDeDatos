import pymysql
class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="Password.03",
            db="miopers1"
        )
        
        
        self.cursor = self.connection.cursor()
        print("Conexión Exitosa")
    
    def selectOne (self, sql):
        try:
            self.cursor.execute(sql)
            edo = self.cursor.fetchone()
            return edo[0]
            
        except Exception as e:
            raise
        
    def selectAll (self, sql):
        try:
            self.cursor.execute(sql)
            edo = self.cursor.fetchall()
            return edo
            
        except Exception as e:
            raise
        
    def update (self, sql):
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print("operación exitosa")
            
        except Exception as e:
            raise
    
    def nTema (self, tema, actualizar, diccionario,):
        sql = "INSERT INTO temas (tema, actualizar, diccionario_tema) values ('{}', {}, '{}');".format(tema, actualizar, diccionario)
        self.update(sql)
    
    def nAnalisisTema (self, idTema, descripcion, path, dicc, actualizar):
        if dicc:
            sql = "INSERT INTO analisis_por_temas (id_tema, descripcion_analisis, path_analisis, diccionario_analisis, actualizar) values ({},'{}', '{}', '{}',{});".format(idTema, descripcion, path, dicc, actualizar)
        else:
            sql = "INSERT INTO analisis_por_temas (id_tema, descripcion_analisis, path_analisis, diccionario_analisis, actualizar) values ({},'{}', '{}',NULL,{});".format(idTema, descripcion, path, actualizar)   
        self.update(sql)
        
    def getCurrentProceso (self):
        sql = "SELECT max(id_proceso) from proceso;"
        return self.selectOne(sql)
    
    def getIdAnalisis (self, analisis):
        sql = "SELECT id_analisis FROM analisis_por_temas WHERE descripcion_analisis LIKE '{}';".format(analisis)
        return self.selectOne(sql)
    
    def getAnalisisDicc (self, analisis):
        sql = "SELECT diccionario_analisis FROM analisis_por_temas WHERE descripcion_analisis LIKE '{}';".format(analisis)
        return self.selectOne(sql)
    
    def getAllAnalisisTopic (self, analisis):
        #obtiene todas las descripciones con sus ids a partir del nombre del analisis
        sql = "SELECT ad.id_detalle, ad.descripcion FROM analisis_detalle ad, analisis_por_temas apt where ad.id_analisis = apt.id_analisis and apt.descripcion_analisis like '{}';".format(analisis)
        return self.selectAll(sql)
    
    def getIDLoc (self,lugar):
        sql = "SELECT id_localidad FROM localidad WHERE nombre LIKE '{}';".format(lugar)
        return self.selectOne(sql)
    
    def getAllLocChild(self,id_locPadre) -> dict():
        sql = "SELECT nombre, id_localidad FROM  localidad WHERE id_loc_padre = {};".format(id_locPadre)
        mun = dict()
        for t in self.db.selectAll(sql):
            mun[t[0]] = t[1]
        
        return mun
            
    def close (self):
        self.connection.close()