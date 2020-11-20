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

        if not query.exec_('CREATE TABLE IF NOT EXISTS historial (idEntrada INTEGER, url TEXT NOT NULL, titulo TEXT, fecha '
                    'TEXT NOT NULL, hora TEXT NOT NULL, PRIMARY KEY(idEntrada AUTOINCREMENT));'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_fav_url ON favoritos (url);'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_fecha ON historial (fecha DESC);'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_hora ON historial (hora ASC);'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_titulo ON historial (titulo ASC);'):
            print(query.lastError().text())

        if not query.exec_('CREATE INDEX IF NOT EXISTS idx_url ON historial (url);'):
            print(query.lastError().text())
    except Exception as error:
        print("Error al crear tablas de BD: %s" % str(error))

def insertar_historial(loadok, url, titulo=""):
    try:
        if loadok:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO historial (url, titulo, fecha, hora) VALUES "
                          "(:url, :titulo, :fecha, :hora);")
            query.bindValue(":url", url)
            query.bindValue(":titulo", titulo)
            now = datetime.now()
            query.bindValue(":fecha", now.strftime("%d/%m/%Y"))
            query.bindValue(":hora", now.strftime("%H:%M"))

            if not query.exec_():
                print("Error: %s" % query.lastError().text())
    except Exception as error:
        print("Error al insertar historial: %s" % str(error))

def cargar_historial():
    try:
        index = 1
        query = QtSql.QSqlQuery()
        query.prepare("SELECT url, titulo, fecha, hora FROM historial ORDER BY fecha DESC, hora DESC")

        if query.exec_():
            while query.next():
                var.dlgHistorial.ui.tableWidget.setRowCount(index)
                var.dlgHistorial.ui.tableWidget.setItem(index - 1, 0, QtWidgets.QTableWidgetItem(query.value(1)))
                var.dlgHistorial.ui.tableWidget.setItem(index - 1, 1, QtWidgets.QTableWidgetItem(query.value(2)))
                var.dlgHistorial.ui.tableWidget.setItem(index - 1, 2, QtWidgets.QTableWidgetItem(query.value(3)))
                var.dlgHistorial.ui.tableWidget.setItem(index - 1, 3, QtWidgets.QTableWidgetItem(query.value(0)))
                index += 1
    except Exception as error:
        print("Error al cargar historial %s" % str(error))