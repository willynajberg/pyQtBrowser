import conexion
import re
import sys
import var

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from WidgetHistorial import WidgetHistorial
from ventana import *


class Main(QMainWindow):
    class HiloHistorial(QThread):
        historialRecibido = QtCore.pyqtSignal(object)
        favoritosRecibidos = QtCore.pyqtSignal(object)
        paginaFavorita = QtCore.pyqtSignal(bool)

        def __init__(self):
            super(Main.HiloHistorial, self).__init__()
            self.running = False
            self.tareas = []

        def run(self):
            conexion.conectardb(var.NOMBRE_BD)
            self.running = True

            while self.running:
                for tarea in self.tareas:
                    tarea()
                    self.tareas.remove(tarea)

                # Ahorra recursos reduciendo la frecuencia con la que se ejecuta el hilo
                self.msleep(20)

        def anadir_tarea(self, tarea):
            self.tareas.append(tarea)

            if not self.running:
                self.start()

        def anadir_historial(self, navegador):
            no_insertar = conexion.seleccionar_ultima_url() and str(conexion.seleccionar_ultima_url()) == str(
                navegador.url().toString())

            if not no_insertar:
                conexion.insertar_historial(navegador.url().toString(), navegador.page().title())
            else:
                conexion.cambiar_titulo_historial(var.LAST_INSERT_HISTORIAL, navegador.page().title())

        def cargar_historial(self):
            query = conexion.cargar_historial()

            try:
                self.historialRecibido.emit(query)
            except Exception as error:
                print("Error: %s" % str(error))

        def cargar_favoritos(self):
            query = conexion.cargar_favoritos()

            try:
                self.favoritosRecibidos.emit(query)
            except Exception as error:
                print("Error: %s" % str(error))

        def comprobar_favorito(self, url):
            es_fav = conexion.comprobar_favorito(url)

            self.paginaFavorita.emit(es_fav)

        def borrar_entrada(self, idx):
            conexion.borrar_entrada_historial(idx)

        def parar(self):
            while len(self.tareas) > 0:
                continue

            self.running = False

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_MainWindow()
        var.ui.setupUi(self)

        var.carga_finalizada = False
        var.progreso_actual = 0

        var.menu = QMenu(var.ui.btnMenu)
        var.menu.addAction(var.ui.actionNewTab)
        var.menu.addAction(var.ui.actionCloseTab)
        var.menu.addSeparator()
        var.menu.addAction(var.ui.actionHistorial)
        var.menu.addAction(var.ui.actionMostrar_marcadores)
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

        # al principio deshabilita los botones de atras y de delante
        var.ui.btnAtras.setDisabled(True)
        var.ui.btnAdelante.setDisabled(True)

        self.hilo_historial = Main.HiloHistorial()

        self.hilo_historial.favoritosRecibidos.connect(self.mostrar_favoritos)
        self.cargar_favoritos()

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
        except Exception as error:
            print("Error: %s" % str(error))

    def conectar_nav(self, navegador):
        try:
            navegador.page().urlChanged.connect(lambda qurl, nav=navegador:
                                                self.cambiar_url(qurl, nav))
            navegador.page().iconChanged.connect(lambda icon, nav=navegador:
                                                 self.actualizar_icono(icon, nav))

            navegador.page().loadStarted.connect(lambda nav=navegador: self.carga_iniciada(nav))
            navegador.page().loadProgress.connect(lambda progreso, nav=navegador: self.progreso_carga(progreso, nav))
            navegador.page().loadFinished.connect(lambda _, nav=navegador: self.carga_completada(nav))
        except Exception as error:
            print("Error: %s" % str(error))

    def carga_iniciada(self, navegador):
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
            self.hilo_historial.anadir_tarea(lambda nav=navegador: self.hilo_historial.anadir_historial(nav))

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
            if icono:
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

    def actualizar_icono_fav(self, es_fav=False):
        try:
            if es_fav:
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("img/star_blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                var.ui.btnFav.setIcon(icon)
                if var.ui.btnFav.receivers(var.ui.btnFav.clicked) > 0:
                    var.ui.btnFav.clicked.disconnect()
            else:
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("img/star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                var.ui.btnFav.setIcon(icon)
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
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("img/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                var.ui.btnRefrescar.setIcon(icon)
                var.ui.btnRefrescar.clicked.connect(self.cancelar_actualizacion)
            else:
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("img/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                var.ui.btnRefrescar.setIcon(icon)
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
            var.ui.tabWidget.currentWidget().page().setUrl(qurl)
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
                elif isinstance(widget_actual, WidgetHistorial):
                    var.ui.btnAtras.setEnabled(False)
                    var.ui.btnAdelante.setEnabled(False)
                    self.setWindowTitle("PyQtBrowser - Historial")
                    self.actualizar_url("pyqtbrowser:historial")
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

    def abrir_historial(self):
        try:
            historial = WidgetHistorial(self)
            self.setWindowTitle("PyQtBrowser - Historial")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("img/history.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
            i = var.ui.tabWidget.addTab(historial, icon, "Historial")
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
        try:
            if self.hilo_historial.receivers(self.hilo_historial.historialRecibido) > 0:
                self.hilo_historial.historialRecibido.disconnect()
            self.hilo_historial.historialRecibido.connect(historial.cargar_historial)
            self.hilo_historial.anadir_tarea(self.hilo_historial.cargar_historial)
        except Exception as error:
            print("Error al cargar historial: %s" % str(error))

    def borrar_entrada_historial(self, idx, historial):
        self.hilo_historial.anadir_tarea(lambda id=idx: self.hilo_historial.borrar_entrada(idx))
        self.hilo_historial.anadir_tarea(lambda his=historial: self.cargar_historial(his))

    def anadir_favorito(self):
        try:
            curpage = var.ui.tabWidget.currentWidget().page()
            self.hilo_historial.anadir_tarea(lambda pag=curpage:
                                             conexion.anadir_favorito(pag))
            self.insertar_marcador(curpage.title(), curpage.url().toString(), curpage.icon().pixmap(
                curpage.icon().actualSize(QtCore.QSize(16, 16))))
            self.actualizar_icono_fav(True)
        except Exception as error:
            print("Error al anadir favorito: %s " % str(error))

    def cargar_favoritos(self):
        try:
            self.hilo_historial.anadir_tarea(self.hilo_historial.cargar_favoritos)
        except Exception as error:
            print("Error al cargar favoritos: %s" % str(error))

    def mostrar_favoritos(self, query):
        try:
            while query.next():
                pixmap = QtGui.QPixmap()
                if query.value(4) is not None and not isinstance(query.value(4), str):
                    ba = QtCore.QByteArray(query.value(4))
                    pixmap.loadFromData(ba, "PNG")

                self.insertar_marcador(query.value(2), query.value(1), pixmap)
        except Exception as error:
            print("Error al mostrar favoritos: %s" % str(error))

    def insertar_marcador(self, titulo, url, icono):
        try:
            boton = QtWidgets.QPushButton(var.ui.widgetMarcadores)
            tam = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            tam.setHorizontalStretch(0)
            tam.setVerticalStretch(0)
            tam.setHeightForWidth(boton.sizePolicy().hasHeightForWidth())
            boton.setSizePolicy(tam)
            boton.setMinimumSize(QtCore.QSize(50, 24))
            boton.setMaximumSize(QtCore.QSize(170, 24))

            boton.setStyleSheet(":hover {\n"
                                "    background:rgba(80, 170, 255, 50);\n"
                                "}\n"
                                "\n"
                                ":pressed {\n"
                                "    background:rgba(80, 170, 255, 100);\n"
                                "}\n"
                                "\n"
                                "QPushButton {background: white; border:none; padding: 4px}")
            icon = QIcon()
            icon.addPixmap(icono, QtGui.QIcon.Normal, QtGui.QIcon.Off)
            boton.setIcon(icon)

            text = titulo

            fm = boton.fontMetrics()
            i = len(text)
            while fm.width(text) > 145:
                text = text[:i] + "..."
                i = i - 1

            boton.setText(text)

            var.ui.layoutMarcadores.insertWidget(var.ui.layoutMarcadores.count() - 1, boton)

            boton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

            menu = QMenu(self)
            menu.addAction("Abrir en nueva pestaña", lambda url=url: self.nueva_pestana(url))
            menu.addAction("Borrar marcador")
            menu.addAction("Editar")

            boton.customContextMenuRequested.connect(lambda point, cmenu=menu, btn=boton:
                                                     cmenu.exec_(btn.mapToGlobal(point)))

            boton.clicked.connect(lambda _, url=url: self.navegar_a_url(url))
        except Exception as error:
            print("Error al insertar marcador: %s" % str(error))

    def comprobar_fav(self, url):
        try:
            if self.hilo_historial.receivers(self.hilo_historial.paginaFavorita) > 0:
                self.hilo_historial.paginaFavorita.disconnect()
            self.hilo_historial.paginaFavorita.connect(self.actualizar_icono_fav)
            self.hilo_historial.anadir_tarea(lambda url=url:
                                             self.hilo_historial.comprobar_favorito(url))
        except Exception as error:
            print("Error al comprobar favorito : %s" % str(error))

    def mostrar_menu(self):
        try:
            var.ui.btnMenu.showMenu()
        except Exception as error:
            print("Error: %s" % str(error))

    def toggle_barra_marcadores(self):
        if var.ui.widgetMarcadores.isHidden():
            var.ui.widgetMarcadores.show()
        else:
            var.ui.widgetMarcadores.hide()


if __name__ == '__main__':
    app = QApplication([])
    var.nav = Main()
    var.nav.showMaximized()

    sys.exit(app.exec())
