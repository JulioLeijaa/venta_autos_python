import pymysql
import warnings

class MySQL():
    def __init__(self):
        warnings.filterwarnings('ignore')
        self.conexion = pymysql.connect(host='localhost',user='root',password='')
        self.cursor = self.conexion.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS venta_autos CHARACTER SET utf8 COLLATE utf8_general_ci")
        self.cursor.execute("USE venta_autos")

        tabla_empleados ="""CREATE TABLE IF NOT EXISTS empleados(
            id int AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            salario int,
            bono int,
            comisiones int)"""
        self.cursor.execute(tabla_empleados)

        tabla_autos = """CREATE TABLE IF NOT EXISTS autos(
            id int AUTO_INCREMENT PRIMARY KEY,
            marca VARCHAR(255) NOT NULL,
            modelo VARCHAR(255) NOT NULL,
            precio int NOT NULL,
            comision int,
            id_empleado int, FOREIGN KEY (id_empleado) REFERENCES empleados(id))"""
        self.cursor.execute(tabla_autos)

    def insertarEmpleado(self, empleado):
        sql="""INSERT INTO empleados(nombre, salario, bono, comisiones) 
            VALUES('{}',{},{},{})""".format(empleado.getNombre(), empleado.getSalario(), empleado.getBono(), empleado.getComisiones())
        self.cursor.execute(sql)
        self.conexion.commit()

        sql2="SELECT id FROM empleados ORDER BY id DESC LIMIT 1"
        self.cursor.execute(sql2)
        self.id_empleado = self.cursor.fetchone()
        self.id_empleado = self.id_empleado[0]

    def insertarAuto(self, auto, bono, comisiones):
        sql="""INSERT INTO autos(marca, modelo, precio, comision, id_empleado) 
            VALUES('{}','{}',{},{},{})""".format(auto.getMarca(), auto.getModelo(), auto.getPrecio(), auto.getComision(), self.id_empleado)
        self.cursor.execute(sql)
        self.conexion.commit()

        sql="UPDATE empleados SET bono = {}, comisiones = {} WHERE id = '{}'".format(bono, comisiones, self.id_empleado)
        self.cursor.execute(sql)
        self.conexion.commit()

    def consultaEmpleado(self):
        sql="""SELECT empleados.id AS id, empleados.nombre AS Nombre,empleados.salario AS Salario,empleados.bono AS Bono ,empleados.comisiones AS Comisiones,count(autos.id_empleado) AS Autos_vendidos 
            FROM empleados join autos on empleados.id = autos.id_empleado"""
        self.cursor.execute(sql)
        for fila in self.cursor:
            print (fila)

    def cerrarConexion(self):
        self.cursor.close()