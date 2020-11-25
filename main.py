import conexion
import re
import sys
import var
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from WidgetHistorial import WidgetHistorial
from ventana import *


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_MainWindow()
        var.nav = self
        var.ui.setupUi(self)

        var.carga_finalizada = False
        var.progreso_actual = 0

        self.nueva_pestana(var.URL_HOME)

        var.menu = QMenu(var.ui.btnMenu)
        var.menu.addAction(var.ui.actionNewTab)
        var.menu.addAction(var.ui.actionCloseTab)
        var.menu.addSeparator();
        var.menu.addAction(var.ui.actionSalir)
        var.ui.btnMenu.setMenu(var.menu)

        # conexión de funciones con eventos del navegador:
        var.ui.editUrl.returnPressed.connect(self.navegar_a_url)
        var.ui.tabWidget.currentChanged.connect(self.pestana_cambiada)
        var.ui.tabWidget.tabCloseRequested.connect(self.cerrar_pestana)
        var.ui.btnHome.clicked.connect(self.navegar_a_home)
        var.ui.btnRefrescar.clicked.connect(self.refrescar)
        var.ui.btnAtras.clicked.connect(lambda: var.ui.tabWidget.currentWidget().back())
        var.ui.btnAdelante.clicked.connect(lambda: var.ui.tabWidget.currentWidget().forward())
        var.ui.btnMenu.clicked.connect(self.mostrar_menu)
        var.ui.btnHist.clicked.connect(self.abrir_historial)

        # conexion de funciones con acciones del navegador
        var.ui.actionNewTab.triggered.connect(lambda: self.nueva_pestana(var.URL_HOME))
        var.ui.actionCloseTab.triggered.connect(lambda: self.cerrar_pestana(var.ui.tabWidget.indexOf(
            var.ui.tabWidget.currentWidget())))
        var.ui.actionSalir.triggered.connect(self.close)

        # al principio deshabilita los botones de atras y de delante
        var.ui.btnAtras.setDisabled(True)
        var.ui.btnAdelante.setDisabled(True)

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
            no_insertar = conexion.seleccionar_ultima_url() and str(conexion.seleccionar_ultima_url()) == str(navegador.url().toString())

            if not no_insertar:
                conexion.insertar_historial(True, navegador.url().toString(), navegador.page().title())
            else:
                conexion.cambiar_titulo_historial(var.LAST_INSERT_HISTORIAL, navegador.page().title())

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
        # cambiara la barra de url del navegador, el icono de la pestana, habilitará los botones de atras y adelante
        # si es posible
        try:
            if navegador == var.ui.tabWidget.currentWidget():
                self.actualizar_icono(None, navegador)
                self.actualizar_url(url)

                var.ui.btnAtras.setEnabled(navegador.history().canGoBack())
                var.ui.btnAdelante.setEnabled(navegador.history().canGoForward())
        except Exception as error:
            print("Error: %s" % str(error))

    def actualizar_url(self, url):
        try:
            var.ui.editUrl.setText(url.toString())
            # Asegura que veremos el principio de la url en el LineEdit
            var.ui.editUrl.setCursorPosition(0)
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

    def navegar_a_url(self):
        # Esta funcion esta conectada al evento returnPressed del lineEdit de la barra de URL. Es decir, se activara
        # cuando el usuario pulse Enter en la barra de url.
        try:
            # Coge el texto del line edit
            url = var.ui.editUrl.text()

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
                    self.actualizar_url(widget_actual.url())

                    var.ui.btnAtras.setEnabled(widget_actual.history().canGoBack())
                    var.ui.btnAdelante.setEnabled(widget_actual.history().canGoForward())
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

            conexion.cargar_historial(historial)

            # para que la pestaña de añadir pestañas aparezca al final, la borra y la vuelve a añadir
            var.ui.tabWidget.removeTab(var.ui.tabWidget.indexOf(var.ui.tabAnadir))
            i2 = var.ui.tabWidget.addTab(var.ui.tabAnadir, "+")

            # esta funcion oculta el boton de cerrar de la pestaña de añadir
            var.ui.tabWidget.tabBar().tabButton(i2, var.ui.tabWidget.tabBar().RightSide).resize(0, 0)
        except Exception as error:
            print("Error al abrir historial: %s" % str(error))

    def mostrar_menu(self):
        try:
            var.ui.btnMenu.showMenu()
        except Exception as error:
            print("Error: %s" % str(error))


if __name__ == '__main__':
    app = QApplication([])
    conexion.conectardb(var.NOMBRE_BD)
    window = Main()
    window.showMaximized()

    sys.exit(app.exec())
