from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from ventana import *

import sys, var, re

URL_HOME = "https://www.google.es/"
URL_BUSQUEDA = "http://www.google.es/search?query=%s"


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_MainWindow()
        var.ui.setupUi(self)
        self.nueva_pestana(URL_HOME)

        var.ui.editUrl.returnPressed.connect(self.navegar_a_url)
        var.ui.tabWidget.currentChanged.connect(self.pestana_cambiada)
        var.ui.tabWidget.tabCloseRequested.connect(self.cerrar_pestana)
        var.ui.btnHome.clicked.connect(self.navegar_a_home)
        var.ui.btnRefrescar.clicked.connect(self.refrescar)
        var.ui.btnAtras.clicked.connect(lambda: var.ui.tabWidget.currentWidget().back())
        var.ui.btnAdelante.clicked.connect(lambda: var.ui.tabWidget.currentWidget().forward())

        var.ui.btnAtras.setDisabled(True)
        var.ui.btnAdelante.setDisabled(True)

    def nueva_pestana(self, url):
        try:
            navegador = QWebEngineView()
            self.setWindowTitle("PyQtBrowser - Pestaña nueva")
            i = var.ui.tabWidget.addTab(navegador, "Pestaña nueva")
            var.ui.tabWidget.setCurrentIndex(i)

            navegador.setUrl(QUrl(url))
            var.ui.editUrl.setText(url)

            navegador.urlChanged.connect(lambda qurl, nav=navegador:
                                         self.actualizar_url(qurl, nav))

            navegador.iconChanged.connect(lambda icon, nav=navegador:
                                          self.actualizar_icono(icon, nav))

            navegador.loadStarted.connect(lambda: self.cambiar_btnrefrescar(True))

            navegador.loadFinished.connect(lambda _, nav=navegador:
                                           self.actualizar_titulo(nav))

            navegador.loadFinished.connect(self.actualizacion_completada)

            var.ui.tabWidget.removeTab(var.ui.tabWidget.indexOf(var.ui.tabAnadir))
            i2 = var.ui.tabWidget.addTab(var.ui.tabAnadir, "+")

            var.ui.tabWidget.tabBar().tabButton(i2, var.ui.tabWidget.tabBar().RightSide).resize(0, 0)
        except Exception as error:
            print("Error: %s" % str(error))

    def actualizar_titulo(self, navegador):
        try:
            titulo = navegador.page().title()
            fm = var.ui.tabWidget.fontMetrics()

            i = len(titulo)
            while fm.width(titulo) > 185:
                titulo = titulo[:i] + "..."
                i = i - 1

            if navegador == var.ui.tabWidget.currentWidget():
                self.setWindowTitle("PyQtBrowser - %s" % titulo)

            var.ui.tabWidget.setTabText(var.ui.tabWidget.indexOf(navegador), titulo)
        except Exception as error:
            print("Error: %s" % str(error))

    def actualizar_icono(self, icono, navegador):
        try:
            var.ui.tabWidget.setTabIcon(var.ui.tabWidget.indexOf(navegador), icono)
        except Exception as error:
            print("Error: %s" % str(error))

    def actualizar_url(self, url, navegador):
        try:
            if navegador == var.ui.tabWidget.currentWidget():
                var.ui.editUrl.setText(url.toString())
                var.ui.editUrl.setCursorPosition(0)

                var.ui.btnAtras.setEnabled(navegador.history().canGoBack())
                var.ui.btnAdelante.setEnabled(navegador.history().canGoForward())
        except Exception as error:
            print("Error: %s" % str(error))

    def cambiar_btnrefrescar(self, cargando):
        try:
            if cargando:
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("img/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                var.ui.btnRefrescar.setIcon(icon)
                var.ui.btnRefrescar.clicked.disconnect()
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
        try:
            var.ui.tabWidget.currentWidget().reload()
        except Exception as error:
            print("Error: %s" % str(error))

    def actualizacion_completada(self):
        try:
            self.cambiar_btnrefrescar(False)
        except Exception as error:
            print("Error: %s" % str(error))

    def cancelar_actualizacion(self):
        try:
            var.ui.tabWidget.currentWidget().stop()
            self.actualizacion_completada()
        except Exception as error:
            print("Error: %s" % str(error))

    def navegar_a_url(self):
        try:
            url = var.ui.editUrl.text()
            es_enlace = re.search("[a-z][.][a-z]", url)
            if es_enlace:
                qurl = QUrl(url)
                if qurl.scheme() == "":
                    qurl.setScheme("http")
            else:
                qurl = QUrl(URL_BUSQUEDA % url.replace(" ", "+"))

            var.ui.tabWidget.currentWidget().setUrl(qurl)
        except Exception as error:
            print("Error: %s" % str(error))

    def navegar_a_home(self):
        try:
            var.ui.tabWidget.currentWidget().setUrl(QUrl(URL_HOME))
        except Exception as error:
            print("Error: %s" % str(error))

    def pestana_cambiada(self, i):
        try:
            if i == var.ui.tabWidget.indexOf(var.ui.tabAnadir):
                self.nueva_pestana(URL_HOME)
            else:
                widget_actual = var.ui.tabWidget.currentWidget()
                self.cambiar_btnrefrescar(False)
                self.actualizar_titulo(widget_actual)
                self.actualizar_url(widget_actual.url(), widget_actual)

                var.ui.btnAtras.setEnabled(widget_actual.history().canGoBack())
                var.ui.btnAdelante.setEnabled(widget_actual.history().canGoForward())
        except Exception as error:
            print("Error: %s" % str(error))

    def cerrar_pestana(self, i):
        try:
            if i == var.ui.tabWidget.indexOf(var.ui.tabAnadir):
                return
            else:
                if var.ui.tabWidget.count() > 2:
                    if i + 1 == var.ui.tabWidget.indexOf(var.ui.tabAnadir):
                        var.ui.tabWidget.setCurrentIndex(i - 1)
                var.ui.tabWidget.removeTab(i)
        except Exception as error:
            print("Error: %s" % str(error))


if __name__ == '__main__':
    app = QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
