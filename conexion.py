from PyQt5 import QtSql
from datetime import datetime
import var
import os
import pathlib
from ventana import *


def conectardb(dbname):
    """

    Establece una conexión con la base de datos de usuario en el hilo actual.

    :param dbname: Nombre del archivo de base de datos
    :type dbname: str
    """
    try:
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        rootPath = str(os.getenv("APPDATA") + "\\pyQtBrowser\\")

        if not os.path.exists(rootPath):
            os.makedirs(rootPath)

        db.setDatabaseName(rootPath + dbname)
        if db.open():
            print('Conexión Establecida')
            crear_tablas()
    except Exception as error:
        print("Error conexion a base de datos: %s" % str(error))


def crear_tablas():
    """

    Ejecuta los queries necesarios para crear las tablas en la base de datos.

    """
    try:
        query = QtSql.QSqlQuery()
        if not query.exec_(
                'CREATE TABLE IF NOT EXISTS favoritos (idEntrada INTEGER NOT NULL, url TEXT NOT NULL, titulo '
                'TEXT, icono BLOB, PRIMARY KEY(idEntrada AUTOINCREMENT));'):
            print(query.lastError().text())

        if not query.exec_('CREATE TABLE IF NOT EXISTS historial (idEntrada INTEGER, url TEXT NOT NULL, titulo TEXT, '
                           'fecha TEXT NOT NULL, hora TEXT NOT NULL, PRIMARY KEY(idEntrada AUTOINCREMENT));'):
            print(query.lastError().text())

        if not query.exec_('CREATE TABLE IF NOT EXISTS preferencias (mostrarfav INTEGER);'):
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
    """

    Inserta una entrada nueva en el historial a partir de los parámetros pasados en argumentos.

    :param url: URL de la entrada
    :type url: str
    :param titulo: Título de la entrada
    :type titulo: str

    Tras insertar la nueva entrada, selecciona su identificador y establece la variable global LAST_INSERT_HISTORIAL
    a ese identificador, para posteriores operaciones.
    """
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
    """

    Recoge la última URL que se insertó en el historial en la base de datos, usando el comando de SQL
    last_insert_rowid()

    :return: Última URL insertada en el historial
    :rtype: str
    """
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


def cambiar_titulo_historial(idx, titulo=""):
    """

    Cambia el título que se ha puesto en una entrada de historial.

    :param idx: Índice de la entrada a cambiar
    :type idx: int
    :param titulo: Nuevo título a poner a la entrada
    :type titulo: str
    """
    try:
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE historial SET titulo=:titulo WHERE idEntrada=:id")
        query.bindValue(":titulo", titulo)
        query.bindValue(":id", idx)
        query.exec_()
    except Exception as error:
        print("Error al cambiar titulo historial: %s" % str(error))


def cargar_historial():
    """

    Selecciona todas las entradas en el historial en la base de datos en orden descendiente y devuelve el resultado del
    query.

    :return: Resultado del query
    :rtype: QtSql.QSqlQuery
    """
    try:
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM historial ORDER BY idEntrada DESC")
        if query.exec_():
            return query
    except Exception as error:
        print("Error al cargar historial %s" % str(error))


def borrar_entrada_historial(idx):
    """

    Borra una entrada del historial en la base de datos.

    :param idx: Índice de la entrada a borrar
    :type idx: int
    """
    try:
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM historial WHERE idEntrada=:id")
        query.bindValue(":id", idx)

        if not query.exec_():
            print(query.lastError())
    except Exception as error:
        print("Error al borrar historial: %s" % str(error))


def anadir_favorito(pag):
    """

    Añade la página que se le pasa en parámetros a favoritos en la base de datos. Devuelve el identificador de esta
    nueva entrada en la base de datos para posteriores modificaciones.

    :param pag: Página a guardar en favoritos
    :type pag: QtWebEngineWidgets.QWebEnginePage
    :return: Identificador de la página en la base de datos
    :rtype: int
    """
    try:
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO favoritos (url, titulo, icono) VALUES (:url, :titulo, :icono)")
        query.bindValue(":url", pag.url().toString())
        query.bindValue(":titulo", pag.title())
        pixmap = pag.icon().pixmap(pag.icon().actualSize(QtCore.QSize(16, 16)))

        ba = QtCore.QByteArray()
        buff = QtCore.QBuffer(ba)
        buff.open(QtCore.QIODevice.WriteOnly)
        pixmap.save(buff, "PNG")

        query.bindValue(":icono", ba)

        if query.exec_():
            query.prepare("SELECT last_insert_rowid() FROM favoritos")

            if query.exec_():
                if query.next():
                    return query.value(0)
    except Exception as error:
        print("Error al insertar favorito: %s" % str(error))


def editar_favorito(idx, titulo, url):
    """

    Edita una entrada de favoritos en la base de datos con los parametros pasados en argumentos.

    :param idx: Índice de la entrada a editar
    :type idx: int
    :param titulo: Nuevo título de la entrada
    :type titulo: str
    :param url: Nueva URL de la entrada
    :type url: str
    """
    try:
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE favoritos SET titulo=:titulo, url=:url WHERE idEntrada=:idx")
        query.bindValue(":idx", idx)
        query.bindValue(":titulo", titulo)
        query.bindValue(":url", url)

        if not query.exec_():
            print(query.lastError().text())
    except Exception as error:
        print("Error editar favorito: %s" % str(error))


def borrar_favorito(idx):
    """

    Borra una entrada de la tabla de favoritos de la base de datos.

    :param idx: Índice de la entrada a borrar
    :type idx: int
    """
    try:
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM favoritos WHERE idEntrada=:id")
        query.bindValue(":id", idx)

        if not query.exec_():
            print(query.lastError().text())
    except Exception as error:
        print("Error al borrar favorito: %s" % str(error))


def cargar_favoritos():
    """

    Selecciona todas las entradas en la tabla de favoritos de la base de datos en orden ascendiente y devuelve el
    resultado del query.

    :return: Resultado del query
    :rtype: QtSql.QSqlQuery
    """
    try:
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM favoritos ORDER BY idEntrada ASC")

        if query.exec_():
            return query
    except Exception as error:
        print("Error al cargar favoritos: %s" % str(error))


def comprobar_favorito(url):
    """

    Comprueba si la URL pasada en argumentos se encuentra en la tabla de favoritos mediante un query.

    :param url: URL a comprobar.
    :type url: str
    :return: Índice de entrada, si es que existe, si no 0.
    :rtype: int
    """
    try:
        query = QtSql.QSqlQuery()
        query.prepare("SELECT idEntrada FROM favoritos WHERE url=:url")
        query.bindValue(":url", url)

        if query.exec_():
            if query.next():
                return query.value(0)
            else:
                return 0
        else:
            query.lastError().text()
            return 0
    except Exception as error:
        print("Error al comprobar favorito: %s" % str(error))


def actualizar_icono_fav(url, icono):
    """

    Actualiza el icono de la página guardada en favoritos.

    :param url: URL de la página
    :type url: str
    :param icono: Nuevo icono
    :type icono: QIcon
    """
    try:
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE favoritos SET icono=:icono WHERE url=:url")

        pixmap = icono.pixmap(icono.actualSize(QtCore.QSize(16, 16)))

        # Pasa el pixmap del icono a un array de bytes para guardarlo como Blob en la BBDD
        ba = QtCore.QByteArray()
        buff = QtCore.QBuffer(ba)
        buff.open(QtCore.QIODevice.WriteOnly)
        pixmap.save(buff, "PNG")

        query.bindValue(":icono", ba)
        query.bindValue(":url", url)

        if not query.exec_():
            print(query.lastError().text())
    except Exception as error:
        print("Error al actualizar icono favorito: %s" % str(error))
