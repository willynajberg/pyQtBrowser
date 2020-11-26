from PyQt5 import QtSql, Qt
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
        if not query.exec_(
                'CREATE TABLE IF NOT EXISTS favoritos (idEntrada INTEGER NOT NULL, url TEXT NOT NULL, titulo '
                'TEXT, carpeta TEXT NOT NULL, PRIMARY KEY(idEntrada AUTOINCREMENT));'):
            print(query.lastError().text())

        if not query.exec_('CREATE TABLE IF NOT EXISTS historial (idEntrada INTEGER, url TEXT NOT NULL, titulo TEXT, '
                           'fecha TEXT NOT NULL, hora TEXT NOT NULL, PRIMARY KEY(idEntrada AUTOINCREMENT));'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_fav_url ON favoritos (url);'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_fecha ON historial (fecha DESC);'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_hora ON historial (hora DESC);'):
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
        query.prepare("INSERT INTO historial (url, titulo, fecha, hora) VALUES "
                      "(:url, :titulo, :fecha, :hora);")
        query.bindValue(":url", url)
        query.bindValue(":titulo", titulo)
        now = datetime.now()
        query.bindValue(":fecha", now.strftime("%d/%m/%Y"))
        query.bindValue(":hora", now.strftime("%H:%M:%S"))

        if not query.exec_():
            print("Error: %s" % query.lastError().text())
        else:
            query.prepare("SELECT last_insert_rowid() FROM historial")

            if query.exec_():
                if query.next():
                    var.LAST_INSERT_HISTORIAL = query.value(0)
    except Exception as error:
        print("Error al insertar historial: %s" % str(error))


def seleccionar_ultima_url():
    try:
        query = QtSql.QSqlQuery()
        query.prepare("SELECT url FROM historial WHERE idEntrada=last_insert_rowid()")
        if query.exec_():
            if query.next():
                return query.value(0)
            else:
                print(query.lastError().text())
                return None
        else:
            print(query.lastError().text())
            return None
    except Exception as error:
        print("Error al seleccionar ultima url: %s" % str(error))


def cambiar_titulo_historial(id, titulo=""):
    try:
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE historial SET titulo=:titulo WHERE idEntrada=:id")
        query.bindValue(":titulo", titulo)
        query.bindValue(":id", id)
        query.exec_()
    except Exception as error:
        print("Error al cambiar titulo historial: %s" % str(error))


def cargar_historial():
    try:
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM historial ORDER BY idEntrada DESC")
        if query.exec_():
            return query
    except Exception as error:
        print("Error al cargar historial %s" % str(error))


def borrar_entrada_historial(idx):
    try:
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM historial WHERE idEntrada=:id")
        query.bindValue(":id", idx)

        if not query.exec_():
            print(query.lastError())
    except Exception as error:
        print("Error al borrar historial: %s" % str(error))
