import sqlite3 
from sqlite3 import Error
from Empleado import Empleado
class SQLite():
    
    def __init__(self):
        self.conexion = sqlite3.connect('venta_autos.db')
        self.cursor = self.conexion.cursor()
        print('Conexion establecida')

        tabla_empleados ="""CREATE TABLE IF NOT EXISTS empleados(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(255) NOT NULL,
            salario int,
            bono int,
            comisiones int)"""
        self.cursor.execute(tabla_empleados)

        tabla_autos = """CREATE TABLE IF NOT EXISTS autos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca VARCHAR(255) NOT NULL,
            modelo VARCHAR(255) NOT NULL,
            precio int NOT NULL,
            comision int,
            id_empleado int, FOREIGN KEY (id_empleado) REFERENCES empleados(id))"""
        self.cursor.execute(tabla_autos)
                         
    def insertarEmpleado(self,empleado):
        with self.conexion:
            self.cursor.execute("""INSERT INTO empleados(nombre, salario, bono, comisiones) 
            VALUES(:nombre, :salario, :bono, :comisiones)""", {'nombre': empleado.getNombre(), 'salario': empleado.getSalario(), 'bono': empleado.getBono(), 'comisiones': empleado.getComisiones()})

        with self.conexion:
            self.cursor.execute("SELECT id FROM empleados ORDER BY id DESC LIMIT 1")
        
        self.id_empleado = self.cursor.fetchone()
        self.id_empleado = self.id_empleado[0]

    def insertarAuto(self, auto, bono, comisiones):
        with self.conexion:
            self.cursor.execute("""INSERT INTO autos(marca, modelo, precio, comision, id_empleado)
            VALUES(:marca, :modelo, :precio, :comision, :id_empleado)""", {'marca': auto.getMarca(), 'modelo': auto.getModelo(), 'precio': auto.getPrecio(), 'comision':  auto.getComision(), 'id_empleado' : self.id_empleado})
         
            self.cursor.execute("""UPDATE empleados SET bono = :bono WHERE id = :id_empleado""",{'bono': bono, 'comisiones': comisiones, 'id_empleado' : self.id_empleado})
            
    def cerrarConexion(self):
        self.cursor.close()