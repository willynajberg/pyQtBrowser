from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from ventana import *

import sys, var


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_MainWindow()
        var.ui.setupUi(self)
        self.nueva_pestana("https://www.google.es/", "Google")

    def nueva_pestana(self, url, titulo):
        navegador = QWebEngineView()
        navegador.setUrl(QUrl(url))
        i = var.ui.tabWidget.addTab(navegador, titulo)
        var.ui.tabWidget.setCurrentIndex(i)

        var.ui.tabWidget.removeTab(var.ui.tabWidget.indexOf(var.ui.tabAnadir))
        var.ui.tabWidget.addTab(var.ui.tabAnadir, "+")

if __name__ == '__main__':
    app = QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
