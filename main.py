#!/usr/bin/env python3
#!/usr/bin/env bash
import pymysql


class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="Password.03",
            db="mexico"
        )
        print(self.connection)
        
        self.cursor = self.connection.cursor()
        
        print("conexión  exitosa")
    
    def select_edo (self, nukidestado):
        sql = "SELECT nukidestado, chd_estado FROM estado WHERE nukidestado ={}".format(nukidestado)
        
        try:
            self.cursor.execute(sql)
            edo = self.cursor.fetchone()
            
            print("id: ", edo[0])
            print("name: ", edo[1])
            
        except Exception as e:
            raise
    
    def select_all_edo (self):
        sql = "SELECT nukidestado, chd_estado FROM estado"
        try:
            self.cursor.execute(sql)
            edo = self.cursor.fetchall()
            return edo
            
        except Exception as e:
            raise
    
    def insert_edo (self,id, namae):
        sql = "INSERT INTO estado (nukidestado, chd_estado) VALUES ({}, '{}');".format(id, namae)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print("operación exitosa")
            
        except Exception as e:
            raise
    
    def dele_edo (self, id):
        sql = "DELETE FROM estado WHERE nukidestado ={}".format(id)
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print("operación exitosa")
            
        except Exception as e:
            raise
    
    def close (self):
        self.connection.close()
        
        

db = DataBase()


#db.insert_edo(45, "Gatita")
#db.dele_edo(40)

estados = db.select_all_edo()
for edo in estados:
    print("id:", edo[0],"name:", edo[1])
    
db.close()