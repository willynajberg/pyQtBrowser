from PyQt5 import QtSql
from datetime import datetime
import var
from ventana import *

def conectardb(dbname):
    try:
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(dbname)
        if db.open():
            print('Conexión Establecida')
            crear_tablas()
    except Exception as error:
        print("Error conexion a base de datos: %s" % str(error))

def crear_tablas():
    try:
        query = QtSql.QSqlQuery()
        if not query.exec_('CREATE TABLE IF NOT EXISTS favoritos (idEntrada INTEGER NOT NULL, url TEXT NOT NULL, titulo '
                    'TEXT, carpeta TEXT NOT NULL, PRIMARY KEY(idEntrada AUTOINCREMENT));'):
            print(query.lastError().text())

        if not query.exec_('CREATE TABLE IF NOT EXISTS historial (idEntrada INTEGER, url TEXT NOT NULL, titulo TEXT, fechahora '
                    'TEXT NOT NULL, PRIMARY KEY(idEntrada AUTOINCREMENT));'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_fav_url ON favoritos (url);'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_fechahora ON historial (fechahora DESC);'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_titulo ON historial (titulo ASC);'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_url ON historial (url);'):
            print(query.lastError().text())
    except Exception as error:
        print("Error al crear tablas de BD: %s" % str(error))

def insertar_historial(url, titulo=""):
    try:
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO historial (url, titulo, fechahora) VALUES "
                      "(:url, :titulo, :fechahora);")
        query.bindValue(":url", url)
        query.bindValue(":titulo", titulo)
        now = datetime.now()
        query.bindValue(":fechahora", now.strftime("%Y/%m/%d %H:%M:%S"))

        if not query.exec_():
            print("Error: %s" % query.lastError().text())
    except Exception as error:
        print("Error al insertar historial: %s" % str(error))