from PyQt5 import QtSql

import conexion
import re
import sys
import var

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from dlgabout import Ui_dlgAbout
from editar_marcador import Ui_dlgEditMarcador
from widgethistorial import WidgetHistorial
from hilo_trabajador import HiloTrabajador
from ventana import *


class DialogEditMarcador(QtWidgets.QDialog):
    def __init__(self, idx, titulo, url):
        super(DialogEditMarcador, self).__init__()
        self.ui = Ui_dlgEditMarcador()
        self.ui.setupUi(self)

        self.ui.txtTitulo.setText(titulo)
        self.ui.txtURL.setText(url)

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(lambda _, indice=idx:
                                                                                self.ejecutar(indice))
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(lambda: self.close())

    def ejecutar(self, idx):
        var.nav.hilo_trab.anadir_tarea(lambda indice=idx, titulo=self.ui.txtTitulo.text(), url=self.ui.txtURL.text():
                                       var.nav.hilo_trab.editar_favorito(indice, titulo, url))


class DialogAbout(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAbout, self).__init__()
        self.ui = Ui_dlgAbout()
        self.ui.setupUi(self)

        self.ui.lblVersion.setText(var.VERSION)
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(lambda: self.close())


class Main(QMainWindow):
    marcadoresLimpios = pyqtSignal()

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_MainWindow()
        var.ui.setupUi(self)

        settings = QSettings("pyQtBrowser", "pyQtBrowser")

        # Menu de la esquina de la derecha:
        var.menu = QMenu(var.ui.btnMenu)
        var.menu.addAction(var.ui.actionNewTab)
        var.menu.addAction(var.ui.actionCloseTab)
        var.menu.addSeparator()
        var.menu.addAction(var.ui.actionHistorial)
        var.menu.addAction(var.ui.actionMostrar_marcadores)
        var.menu.addSeparator()
        var.menu.addAction(var.ui.actionAbrir)
        var.menu.addAction(var.ui.actionGuardar)
        var.menu.addAction(var.ui.actionImprimir)
        var.menu.addAction(var.ui.actionBuscar)
        var.menu.addSeparator()
        var.menu.addAction(var.ui.actionAcerca_de)
        var.menu.addSeparator()
        var.menu.addAction(var.ui.actionSalir)
        var.ui.btnMenu.setMenu(var.menu)

        # conexión de funciones con eventos del navegador:
        var.ui.editUrl.returnPressed.connect(lambda: self.navegar_a_url(var.ui.editUrl.text()))
        var.ui.tabWidget.currentChanged.connect(self.pestana_cambiada)
        var.ui.tabWidget.tabCloseRequested.connect(self.cerrar_pestana)
        var.ui.btnHome.clicked.connect(self.navegar_a_home)
        var.ui.btnRefrescar.clicked.connect(self.refrescar)
        var.ui.btnAtras.clicked.connect(lambda: var.ui.tabWidget.currentWidget().back())
        var.ui.btnAdelante.clicked.connect(lambda: var.ui.tabWidget.currentWidget().forward())
        var.ui.btnMenu.clicked.connect(self.mostrar_menu)
        var.ui.btnHist.clicked.connect(self.abrir_historial)
        var.ui.btnFav.clicked.connect(self.anadir_favorito)

        # conexion de funciones con acciones del navegador
        var.ui.actionNewTab.triggered.connect(lambda: self.nueva_pestana(var.URL_HOME))
        var.ui.actionCloseTab.triggered.connect(lambda: self.cerrar_pestana(var.ui.tabWidget.indexOf(
            var.ui.tabWidget.currentWidget())))
        var.ui.actionHistorial.triggered.connect(self.abrir_historial)
        var.ui.actionSalir.triggered.connect(self.close)
        var.ui.actionMostrar_marcadores.triggered.connect(lambda _, sett=settings: self.toggle_barra_marcadores(sett))
        var.ui.actionAbrir.triggered.connect(self.abrir_pagina)
        var.ui.actionGuardar.triggered.connect(self.guardar_pagina)
        var.ui.actionAcerca_de.triggered.connect(self.abrir_about)

        var.ui.widgetMarcadores = QToolBar()
        var.ui.widgetMarcadores.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        var.ui.verticalLayout.insertWidget(1, var.ui.widgetMarcadores)

        if settings.value("mostrarMarcadores", False, bool):
            var.ui.widgetMarcadores.show()
            var.ui.actionMostrar_marcadores.setText("Ocultar barra de marcadores")
        else:
            var.ui.widgetMarcadores.hide()
            var.ui.actionMostrar_marcadores.setText("Mostrar barra de marcadores")

        # al principio deshabilita los botones de atras y de delante
        var.ui.btnAtras.setDisabled(True)
        var.ui.btnAdelante.setDisabled(True)

        # Crea una nueva instancia del hilo trabajador
        self.hilo_trab = HiloTrabajador()

        # Conecta la señal emitida por el hilo al recibir las paginas favoritas de la BD con la funcion del navegador
        self.hilo_trab.favoritosRecibidos.connect(self.cargar_favoritos)
        self.hilo_trab.anadir_tarea(self.hilo_trab.cargar_favoritos)

        self.nueva_pestana(var.URL_HOME)

    def nueva_pestana(self, url):
        try:
            # crea un objeto QWebEngineView nuevo y lo asignamos a una pestaña nueva del TableWidget
            navegador = QWebEngineView()

            self.setWindowTitle("PyQtBrowser - Pestaña nueva")
            i = var.ui.tabWidget.addTab(navegador, "Pestaña nueva")
            var.ui.tabWidget.setCurrentIndex(i)

            # cargamos la url nueva en el nuevo objeto y en la barra de urls
            navegador.page().setUrl(QUrl(url))
            var.ui.editUrl.setText(url)

            # conexion de eventos del objeto QWebEngineView con funciones del navegador
            self.conectar_nav(navegador)

            # para que la pestaña de añadir pestañas aparezca al final, la borra y la vuelve a añadir
            var.ui.tabWidget.removeTab(var.ui.tabWidget.indexOf(var.ui.tabAnadir))
            i2 = var.ui.tabWidget.addTab(var.ui.tabAnadir, "+")

            # esta funcion oculta el boton de cerrar de la pestaña de añadir
            var.ui.tabWidget.tabBar().tabButton(i2, var.ui.tabWidget.tabBar().RightSide).resize(0, 0)

            return navegador
        except Exception as error:
            print("Error: %s" % str(error))
            return None

    def conectar_nav(self, navegador):
        try:
            navegador.urlChanged.connect(lambda qurl, nav=navegador:
                                         self.cambiar_url(qurl, nav))
            navegador.iconChanged.connect(lambda icono, nav=navegador:
                                          self.actualizar_icono(icono, nav))

            navegador.loadStarted.connect(lambda nav=navegador: self.carga_iniciada(nav))
            navegador.loadProgress.connect(lambda progreso, nav=navegador: self.progreso_carga(progreso, nav))
            navegador.loadFinished.connect(lambda _, nav=navegador: self.carga_completada(nav))

            # Sobreescribe la funcion de createWindow del QWebEngineView con la definida abajo
            # Esta funcion es llamada por elementos javascript de las paginas que abren ventanas nuevas
            navegador.createWindow = self.crear_window
        except Exception as error:
            print("Error: %s" % str(error))

    def crear_window(self, t):
        # Al intentar crear una pestaña nueva con javascript, este espera que el navegador en el que se ejecuta le
        # retorne un puntero a un objeto de tipo QWebEnginePage en el que pueda escribir una url nueva
        try:
            nueva = self.nueva_pestana("")
            nuevapag = QWebEnginePage()
            nueva.setAttribute(Qt.WA_NativeWindow, True)
            nueva.setPage(nuevapag)
            nueva.show()

            return nueva
        except Exception as error:
            print("Error: %s" % str(error))

    def carga_iniciada(self, navegador):
        # Al empezar a cargar una página, comprobará si esta página está en los favoritos, y cambiará el boton de
        # refrescar por el de cancelar carga.
        try:
            self.comprobar_fav(navegador.page().url().toString())

            self.cambiar_btnrefrescar(True)
        except Exception as error:
            print("Error: %s" % str(error))

    def progreso_carga(self, progreso, navegador):
        try:
            if progreso == 100:
                # En algunas paginas como YouTube el evento loadFinished no es emitido, la unica forma que he encontrado
                # de solucionar esto es con un timer
                QTimer.singleShot(1000, lambda nav=navegador: self.carga_completada(navegador))
        except Exception as error:
            print("Error: %s" % str(error))

    def carga_completada(self, navegador):
        # Función conectada al evento loadFinished del navegador. Se encargará de cambiar el boton de cancelar carga
        # al de refrescar, de actualizar el título y de insertar una nueva entrada en el historial, o en caso de que
        # la última entrada del historial sea la misma url, actualizar su título
        try:
            if navegador is not None and isinstance(navegador, QWebEngineView):
                self.hilo_trab.anadir_tarea(lambda nav=navegador: self.hilo_trab.anadir_historial(nav))
                self.actualizacion_completada()
                self.actualizar_icono(navegador.page().icon(), navegador)
                self.actualizar_titulo(navegador)
        except Exception as error:
            print("Error en la funcion carga completada: %s" % str(error))

    def actualizar_titulo(self, navegador):
        # Funcion conectada al evento loadFinished de un objeto QWebEngineView. Cuando una página acabe de cargar,
        # cambiará el título de la pestaña asignada a ese QWebEngineView al título de la página web
        try:
            titulo = navegador.page().title()

            if len(titulo) == 0:
                titulo = "Pestaña nueva"
            # Este código se asegurará de que los títulos de páginas largos se acortarán
            fm = var.ui.tabWidget.fontMetrics()
            i = len(titulo)
            while fm.width(titulo) > 185:
                titulo = titulo[:i] + "..."
                i = i - 1

            # Si la pestaña que tenemos abierta es la del QWebEngineView que ha activado el evento, cambia el título
            # de la ventana también
            if navegador == var.ui.tabWidget.currentWidget():
                self.setWindowTitle("PyQtBrowser - %s" % titulo)

            # Cambia el título de la pestaña del QWebEngineView que ha llamado al evento
            var.ui.tabWidget.setTabText(var.ui.tabWidget.indexOf(navegador), titulo)
        except Exception as error:
            print("Error: %s" % str(error))

    def actualizar_icono(self, icono, navegador):
        # Esta función funciona igual que la funcion de actualizar_titulo, solo que en este caso es llamada por el
        # evento iconChanged de un QWebEngine view, y le asignamos el icono de la página a la pestaña
        try:
            if icono and icono is not None:
                self.hilo_trab.anadir_tarea(lambda nav=navegador, i=icono:
                                            conexion.actualizar_icono_fav(nav.page().url().toString(), i))
                var.ui.tabWidget.setTabIcon(var.ui.tabWidget.indexOf(navegador), icono)
            else:
                # si han pasado un icono nulo, pasa un icono en blanco
                var.ui.tabWidget.setTabIcon(var.ui.tabWidget.indexOf(navegador), QIcon())
        except Exception as error:
            print("Error: %s" % str(error))

    def cambiar_url(self, url, navegador):
        # Esta funcion es llamada por el evento urlChanged de un QWebEngineView. Cuando este evento se ejecute
        # cambiara la barra de url del navegador, el icono de la pestana, cambiara el icono de favorito
        # habilitará los botones de atras y adelante si es posible
        try:
            if navegador == var.ui.tabWidget.currentWidget():
                if url.scheme() == "http" or url.scheme() == "https":
                    self.actualizar_icono(None, navegador)
                    self.actualizar_url(url.toString())

                    self.comprobar_fav(url.toString())

                var.ui.btnAtras.setEnabled(navegador.history().canGoBack())
                var.ui.btnAdelante.setEnabled(navegador.history().canGoForward())
        except Exception as error:
            print("Error: %s" % str(error))

    def actualizar_url(self, url):
        try:
            var.ui.editUrl.setText(url)
            # Asegura que veremos el principio de la url en el LineEdit
            var.ui.editUrl.setCursorPosition(0)
        except Exception as error:
            print("Error: %s" % str(error))

    def actualizar_icono_fav(self, id_entrada=0):
        # Esta funcion es la encargada de cambiar la apariencia del botón de favoritos si la página en la que estamos
        # Está marcada como favorita, y desconectará las funciones conectadas a su evento clicked y las reemplazará
        # por las indicadas
        try:
            if id_entrada != 0:
                icono = QtGui.QIcon()
                icono.addPixmap(QtGui.QPixmap("img/star_blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                var.ui.btnFav.setIcon(icono)
                if var.ui.btnFav.receivers(var.ui.btnFav.clicked) > 0:
                    var.ui.btnFav.clicked.disconnect()
                var.ui.btnFav.clicked.connect(lambda _, idx=id_entrada: self.borrar_favorito(idx))
            else:
                icono = QtGui.QIcon()
                icono.addPixmap(QtGui.QPixmap("img/star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                var.ui.btnFav.setIcon(icono)
                if var.ui.btnFav.receivers(var.ui.btnFav.clicked) > 0:
                    var.ui.btnFav.clicked.disconnect()
                var.ui.btnFav.clicked.connect(self.anadir_favorito)
        except Exception as error:
            print("Error: %s" % str(error))

    def cambiar_btnrefrescar(self, cargando):
        # Esta funcion es la encargada de cambiar el botón de refrescar por el de cancelar carga, segun el booleano
        # que se le pase en los parametros
        try:
            if cargando:
                icono = QtGui.QIcon()
                icono.addPixmap(QtGui.QPixmap("img/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                var.ui.btnRefrescar.setIcon(icono)
                var.ui.btnRefrescar.clicked.connect(self.cancelar_actualizacion)
            else:
                icono = QtGui.QIcon()
                icono.addPixmap(QtGui.QPixmap("img/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                var.ui.btnRefrescar.setIcon(icono)
                var.ui.btnRefrescar.clicked.disconnect()
                var.ui.btnRefrescar.clicked.connect(self.refrescar)
        except Exception as error:
            print("Error : %s" % str(error))

    def refrescar(self):
        # Funcion conectada al evento clicked del boton de refrescar. Refresca la página actual y cambia el boton de
        # refrescar por el de cancelar carga
        try:
            var.ui.tabWidget.currentWidget().reload()
        except Exception as error:
            print("Error: %s" % str(error))

    def actualizacion_completada(self):
        # Funcion conectada al evento loadFinished de un QWebEngineView que simplemente cambiará el boton de cancelar
        # carga por el de refrescar de nuevo
        try:
            self.cambiar_btnrefrescar(False)
        except Exception as error:
            print("Error: %s" % str(error))

    def cancelar_actualizacion(self):
        # Funcion conectada al evento clicked del boton de cancelar carga que parará la carga de la pestaña actual
        # y cambiara el boton de cancelar carga por el de refrescar nuevamente
        try:
            var.ui.tabWidget.currentWidget().stop()
            self.actualizacion_completada()
        except Exception as error:
            print("Error: %s" % str(error))

    def navegar_a_url(self, url):
        # Esta funcion esta conectada al evento returnPressed del lineEdit de la barra de URL. Es decir, se activara
        # cuando el usuario pulse Enter en la barra de url.
        try:
            # Usa un patron de RegEx para comprobar si lo que el usuario ha introducido es un enlace o una IP
            es_enlace = re.search("(([a-zA-Z]|[0-9])[.]([a-zA-Z]|[0-9]))|[a-z][/]$", url)

            if es_enlace:
                # Si es un enlace, creara un objeto QUrl con el enlace introducido
                qurl = QUrl(url)

                # Si el usuario no ha puesto http:// o https:// al principio, pondra el protocolo http automaticamente
                if qurl.scheme() == "":
                    qurl.setScheme("http")
            else:
                # Si lo que el usuario ha puesto no es un enlace, reemplaza los espacios en blanco por + y utiliza
                # el enlace de busqueda establecido para buscar lo introducido en internet.
                qurl = QUrl(var.URL_BUSQUEDA % url.replace(" ", "+"))

            # Finalmente cambia a la QUrl generada.
            if isinstance(var.ui.tabWidget.currentWidget(), QWebEngineView):
                var.ui.tabWidget.currentWidget().page().setUrl(qurl)
            else:
                self.nueva_pestana(url)
        except Exception as error:
            print("Error: %s" % str(error))

    def navegar_a_home(self):
        # Funcion conectada al boton home del navegador que simplemente navegara al enlace establecido como enlace home
        try:
            var.ui.tabWidget.currentWidget().setUrl(QUrl(var.URL_HOME))
        except Exception as error:
            print("Error: %s" % str(error))

    def pestana_cambiada(self, i):
        # Funcion conectada al evento tabChanged del TabWidget del navegador que se encarga de cambiar el titulo de la
        # ventana principal, la url del line edit, el boton de refrescar y los botones de atras y adelante.
        try:
            # Si la pestaña a la que el usuario se quiere desplazar es la pestaña de añadir, añade una nueva
            if i == var.ui.tabWidget.indexOf(var.ui.tabAnadir):
                self.nueva_pestana(var.URL_HOME)
            else:
                widget_actual = var.ui.tabWidget.currentWidget()
                if isinstance(widget_actual, QWebEngineView):
                    self.cambiar_btnrefrescar(False)
                    self.actualizar_titulo(widget_actual)
                    self.actualizar_url(widget_actual.url().toString())
                    self.comprobar_fav(widget_actual.url().toString())

                    var.ui.btnAtras.setEnabled(widget_actual.history().canGoBack())
                    var.ui.btnAdelante.setEnabled(widget_actual.history().canGoForward())
                # Si el widget actual es la pestaña de historial, para evitar errores deshabilitará los botones de
                # navegacion
                elif isinstance(widget_actual, WidgetHistorial):
                    var.ui.btnAtras.setEnabled(False)
                    var.ui.btnAdelante.setEnabled(False)
                    self.setWindowTitle("PyQtBrowser - Historial")
                    self.actualizar_url("pyqtbrowser:historial")
                    self.actualizar_icono_fav(0)
        except Exception as error:
            print("Error: %s" % str(error))

    def cerrar_pestana(self, i):
        # Funcion conectada al evento tabCloseRequested del TabWidget del navegador que se activará cuando el usuario
        # cierre una de las pestañas
        try:
            # Si la pestaña a cerrar es la de añadir pestañas no hace nada
            if i == var.ui.tabWidget.indexOf(var.ui.tabAnadir):
                return
            else:
                # Cierra el objeto navegador
                var.ui.tabWidget.widget(i).close()

                # Si la pestaña a cerrar esta justo antes de la de añadir, cambia la vista a una pestaña anterior, si es
                # que la hay
                if var.ui.tabWidget.count() > 2:
                    if i + 1 == var.ui.tabWidget.indexOf(var.ui.tabAnadir):
                        var.ui.tabWidget.setCurrentIndex(i - 1)

                # Finalmente borra la pestaña
                var.ui.tabWidget.removeTab(i)
        except Exception as error:
            print("Error: %s" % str(error))

    def abrir_pagina(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "",
                                                  "Hypertext Markup Language (*.htm *.html)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.nueva_pestana('')
            var.ui.editUrl.setText(filename)
            var.ui.tabWidget.currentWidget().setHtml(html)

    def guardar_pagina(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "Guardar Pagina Como", "",
                                                      "Hypertext Markup Language (*.htm *html);;"
                                                      "Todos los archivos (*.*)")

            if filename:
                var.ui.tabWidget.currentWidget().page().toHtml(lambda html, f=filename:
                                                               self.guardar_html(html, f))
        except Exception as error:
            print("Error en guardar pagina: %s" % str(error))

    def guardar_html(self, html, filename):
        try:
            with open(filename, 'w') as f:
                f.write(html.encode('ascii', 'xmlcharrefreplace').__str__().removeprefix("b'"))
        except Exception as error:
            print("Error en guardar pagina: %s" % str(error))

    def abrir_about(self):
        try:
            dlg = DialogAbout()
            dlg.exec_()
        except Exception as error:
            print("Error en abrir about: %s" % str(error))

    def abrir_historial(self):
        # Funcion encargada de abrir una pestaña nueva que contiene el historial de búsqueda
        try:
            # Crea el objeto del Widget del historial pasándole la ventana del navegador como argumento
            historial = WidgetHistorial(self)

            self.setWindowTitle("PyQtBrowser - Historial")
            icono = QtGui.QIcon()
            icono.addPixmap(QtGui.QPixmap("img/history.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
            i = var.ui.tabWidget.addTab(historial, icono, "Historial")
            var.ui.tabWidget.setCurrentIndex(i)

            var.ui.editUrl.setText("pyqtbrowser:historial")

            self.cargar_historial(historial)

            # para que la pestaña de añadir pestañas aparezca al final, la borra y la vuelve a añadir
            var.ui.tabWidget.removeTab(var.ui.tabWidget.indexOf(var.ui.tabAnadir))
            i2 = var.ui.tabWidget.addTab(var.ui.tabAnadir, "+")

            # esta funcion oculta el boton de cerrar de la pestaña de añadir
            var.ui.tabWidget.tabBar().tabButton(i2, var.ui.tabWidget.tabBar().RightSide).resize(0, 0)
        except Exception as error:
            print("Error al abrir historial: %s" % str(error))

    def cargar_historial(self, historial):
        # Funcion encargada de pasarle una tarea nueva al hilo trabajador del navegador de cargar el historial
        # de la base de datos
        try:
            # Si ya hay una funcion escuchando el evento de historialRecibido, la desconecta
            if self.hilo_trab.receivers(self.hilo_trab.historialRecibido) > 0:
                self.hilo_trab.historialRecibido.disconnect()

            # Conecta el evento del hilo trabajador que emite al recibir el historial de la BD, con la funcion de
            # cargar historial del objeto WidgetHistorial
            self.hilo_trab.historialRecibido.connect(historial.cargar_historial)

            # Añade una tarea de carga de historial al hilo trabajador
            self.hilo_trab.anadir_tarea(self.hilo_trab.cargar_historial)
        except Exception as error:
            print("Error al cargar historial: %s" % str(error))

    def borrar_entrada_historial(self, idx, historial):
        # Esta funcion simplemente le pasa 2 tareas al hilo trabajador: borrar una entrada de historial con indice idx
        # Y volver a cargar el historial en el widget de historial pasado en argumentos

        self.hilo_trab.anadir_tarea(lambda indice=idx: self.hilo_trab.borrar_entrada(indice))
        self.hilo_trab.anadir_tarea(lambda his=historial: self.cargar_historial(his))

    def anadir_favorito(self):
        try:
            if isinstance(var.ui.tabWidget.currentWidget(), QWebEngineView):
                # Obtiene el objeto QWebEnginePage del widget actual
                curpage = var.ui.tabWidget.currentWidget().page()

                if curpage.url().scheme() == "http" or curpage.url().scheme() == "https":
                    # Pasa la tarea de añadir la pagina actual a favoritos a la base de datos al hilo trabajador
                    self.hilo_trab.anadir_tarea(lambda pag=curpage: self.hilo_trab.anadir_favorito(pag))
                    self.hilo_trab.anadir_tarea(self.hilo_trab.cargar_favoritos)

                    # Actualiza el icono del boton de favoritos del navegador
                    self.comprobar_fav(curpage.url())
        except Exception as error:
            print("Error al anadir favorito: %s " % str(error))

    def borrar_favorito(self, id_entrada=0):
        try:
            if id_entrada != 0:
                self.hilo_trab.anadir_tarea(lambda idx=id_entrada: conexion.borrar_favorito(idx))
                self.comprobar_fav(var.ui.tabWidget.currentWidget().page().url())
                self.hilo_trab.anadir_tarea(self.hilo_trab.cargar_favoritos)
        except Exception as error:
            print("Error al borrar favorito: %s " % str(error))

    def cargar_favoritos(self, query):
        # Esta funcion recibe un objeto de QSqlQuery del evento favoritosRecibidos emitido por el hilo trabajador
        # E itera el objeto QSqlQuery para insertar los marcadores en la barra
        try:
            self.limpiar_marcadores()

            if self.receivers(self.marcadoresLimpios) > 0:
                self.marcadoresLimpios.disconnect()

            self.marcadoresLimpios.connect(lambda q=query: self.mostrar_favoritos(q))
        except Exception as error:
            print("Error al mostrar favoritos: %s" % str(error))

    def mostrar_favoritos(self, query):
        try:
            while query.next():
                pixmap = QtGui.QPixmap()
                if query.value(3) is not None and not isinstance(query.value(3), str):
                    ba = QtCore.QByteArray(query.value(3))
                    pixmap.loadFromData(ba, "PNG")

                self.insertar_marcador(query.value(2), query.value(1), pixmap, query.value(0))
        except Exception as error:
            print("Error: %s" % str(error))

    def limpiar_marcadores(self):
        try:
            var.ui.widgetMarcadores.clear()
            QTimer.singleShot(100, self.marcadoresLimpios.emit)
        except Exception as error:
            print("Error al limpiar marcadores: %s" % str(error))

    def insertar_marcador(self, titulo, url, icono, id_entrada):
        # Funcion encargada de crear un boton con los parametros indicados e insertarlo en la barra de marcadores
        try:
            icon = QIcon()
            icon.addPixmap(icono, QtGui.QIcon.Normal, QtGui.QIcon.Off)
            action = QAction(var.ui.widgetMarcadores)
            action.setIcon(icon)

            text = titulo

            fm = var.ui.widgetMarcadores.fontMetrics()
            i = len(text)
            while fm.width(text) > 145:
                text = text[:i] + "..."
                i = i - 1

            action.setText(text)
            action.triggered.connect(lambda _, url=url: self.navegar_a_url(url))

            menu = QMenu(self)
            menu.addAction("Abrir", lambda url=url: self.navegar_a_url(url))
            menu.addAction("Abrir en nueva pestaña", lambda url=url: self.nueva_pestana(url))
            menu.addAction("Borrar marcador", lambda idx=id_entrada: self.borrar_favorito(idx))
            menu.addAction("Editar",
                           lambda idx=id_entrada, titulo=titulo, url=url: self.abrir_editar_marcador(idx, titulo, url))

            action.setMenu(menu)
            var.ui.widgetMarcadores.addAction(action)
        except Exception as error:
            print("Error al insertar marcador: %s" % str(error))

    def abrir_editar_marcador(self, idx, titulo, url):
        try:
            dlg = DialogEditMarcador(idx, titulo, url)
            dlg.exec_()
        except Exception as error:
            print("Error editar marcador: %s" % str(error))

    def comprobar_fav(self, url):
        try:
            if self.hilo_trab.receivers(self.hilo_trab.paginaFavorita) > 0:
                self.hilo_trab.paginaFavorita.disconnect()
            self.hilo_trab.paginaFavorita.connect(self.actualizar_icono_fav)
            self.hilo_trab.anadir_tarea(lambda url=url: self.hilo_trab.comprobar_favorito(url))
        except Exception as error:
            print("Error al comprobar favorito : %s" % str(error))

    def mostrar_menu(self):
        try:
            var.ui.btnMenu.showMenu()
        except Exception as error:
            print("Error: %s" % str(error))

    def toggle_barra_marcadores(self, settings):
        try:
            if var.ui.widgetMarcadores.isHidden():
                var.ui.actionMostrar_marcadores.setText("Ocultar barra de marcadores")
                var.ui.widgetMarcadores.show()
                settings.setValue("mostrarMarcadores", True)
            else:
                var.ui.actionMostrar_marcadores.setText("Mostrar barra de marcadores")
                var.ui.widgetMarcadores.hide()
                settings.setValue("mostrarMarcadores", False)

        except Exception as error:
            print("Error: %s" % str(error))

    def resizeEvent(self, *args, **kwargs):
        # probablemente no sea lo mas eficiente del mundo pero si la opcion mas comoda
        self.hilo_trab.anadir_tarea(self.hilo_trab.cargar_favoritos)


if __name__ == '__main__':
    app = QApplication([])
    QWebEngineSettings.PluginsEnabled = True

    var.nav = Main()
    var.nav.showMaximized()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("img/pyqtbrowser.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
    var.nav.setWindowIcon(icon)

    sys.exit(app.exec())
