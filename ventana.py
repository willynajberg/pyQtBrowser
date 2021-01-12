# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ventana.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("QWidget#centralwidget {background-color:white}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnAtras = QtWidgets.QPushButton(self.centralwidget)
        self.btnAtras.setMinimumSize(QtCore.QSize(26, 26))
        self.btnAtras.setStyleSheet(":hover {\n"
"    background:rgba(80, 170, 255, 50);\n"
"}\n"
"\n"
":pressed {\n"
"    background:rgba(80, 170, 255, 100);\n"
"}\n"
"\n"
"QPushButton {background: white; border:none}")
        self.btnAtras.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/left-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAtras.setIcon(icon)
        self.btnAtras.setFlat(True)
        self.btnAtras.setObjectName("btnAtras")
        self.horizontalLayout.addWidget(self.btnAtras)
        self.btnAdelante = QtWidgets.QPushButton(self.centralwidget)
        self.btnAdelante.setMinimumSize(QtCore.QSize(26, 26))
        self.btnAdelante.setStyleSheet(":hover {\n"
"    background:rgba(80, 170, 255, 50);\n"
"}\n"
"\n"
":pressed {\n"
"    background:rgba(80, 170, 255, 100);\n"
"}\n"
"\n"
"QPushButton {background: white; border:none}")
        self.btnAdelante.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdelante.setIcon(icon1)
        self.btnAdelante.setFlat(True)
        self.btnAdelante.setObjectName("btnAdelante")
        self.horizontalLayout.addWidget(self.btnAdelante)
        self.btnRefrescar = QtWidgets.QPushButton(self.centralwidget)
        self.btnRefrescar.setMinimumSize(QtCore.QSize(26, 26))
        self.btnRefrescar.setStyleSheet(":hover {\n"
"    background:rgba(80, 170, 255, 50);\n"
"}\n"
"\n"
":pressed {\n"
"    background:rgba(80, 170, 255, 100);\n"
"}\n"
"\n"
"QPushButton {background: white; border:none}")
        self.btnRefrescar.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRefrescar.setIcon(icon2)
        self.btnRefrescar.setFlat(True)
        self.btnRefrescar.setObjectName("btnRefrescar")
        self.horizontalLayout.addWidget(self.btnRefrescar)
        self.btnHome = QtWidgets.QPushButton(self.centralwidget)
        self.btnHome.setMinimumSize(QtCore.QSize(26, 26))
        self.btnHome.setStyleSheet(":hover {\n"
"    background:rgba(80, 170, 255, 50);\n"
"}\n"
"\n"
":pressed {\n"
"    background:rgba(80, 170, 255, 100);\n"
"}\n"
"\n"
"QPushButton {background: white; border:none}")
        self.btnHome.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnHome.setIcon(icon3)
        self.btnHome.setFlat(True)
        self.btnHome.setObjectName("btnHome")
        self.horizontalLayout.addWidget(self.btnHome)
        self.editUrl = QtWidgets.QLineEdit(self.centralwidget)
        self.editUrl.setMinimumSize(QtCore.QSize(0, 26))
        self.editUrl.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.editUrl.setClearButtonEnabled(True)
        self.editUrl.setObjectName("editUrl")
        self.horizontalLayout.addWidget(self.editUrl)
        self.btnFav = QtWidgets.QPushButton(self.centralwidget)
        self.btnFav.setMinimumSize(QtCore.QSize(26, 26))
        self.btnFav.setStyleSheet(":hover {\n"
"    background:rgba(80, 170, 255, 50);\n"
"}\n"
"\n"
":pressed {\n"
"    background:rgba(80, 170, 255, 100);\n"
"}\n"
"\n"
"QPushButton {background: white; border:none}")
        self.btnFav.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("img/star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFav.setIcon(icon4)
        self.btnFav.setFlat(True)
        self.btnFav.setObjectName("btnFav")
        self.horizontalLayout.addWidget(self.btnFav)
        self.btnHist = QtWidgets.QPushButton(self.centralwidget)
        self.btnHist.setMinimumSize(QtCore.QSize(26, 26))
        self.btnHist.setStyleSheet(":hover {\n"
"    background:rgba(80, 170, 255, 50);\n"
"}\n"
"\n"
":pressed {\n"
"    background:rgba(80, 170, 255, 100);\n"
"}\n"
"\n"
"QPushButton {background: white; border:none}")
        self.btnHist.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("img/history.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnHist.setIcon(icon5)
        self.btnHist.setFlat(True)
        self.btnHist.setObjectName("btnHist")
        self.horizontalLayout.addWidget(self.btnHist)
        self.btnMenu = QtWidgets.QPushButton(self.centralwidget)
        self.btnMenu.setMinimumSize(QtCore.QSize(26, 26))
        self.btnMenu.setStyleSheet(":hover {\n"
"    background:rgba(80, 170, 255, 50);\n"
"}\n"
"\n"
":pressed {\n"
"    background:rgba(80, 170, 255, 100);\n"
"}\n"
"\n"
"QPushButton {background: white; border:none}\n"
"\n"
"")
        self.btnMenu.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("img/menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnMenu.setIcon(icon6)
        self.btnMenu.setFlat(False)
        self.btnMenu.setObjectName("btnMenu")
        self.horizontalLayout.addWidget(self.btnMenu)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widgetMarcadores = QtWidgets.QWidget(self.centralwidget)
        self.widgetMarcadores.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetMarcadores.sizePolicy().hasHeightForWidth())
        self.widgetMarcadores.setSizePolicy(sizePolicy)
        self.widgetMarcadores.setMinimumSize(QtCore.QSize(0, 28))
        self.widgetMarcadores.setMaximumSize(QtCore.QSize(16777215, 28))
        self.widgetMarcadores.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.widgetMarcadores.setObjectName("widgetMarcadores")
        self.layoutMarcadores = QtWidgets.QHBoxLayout(self.widgetMarcadores)
        self.layoutMarcadores.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.layoutMarcadores.setContentsMargins(6, 0, 6, 0)
        self.layoutMarcadores.setObjectName("layoutMarcadores")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layoutMarcadores.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widgetMarcadores)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("QTabBar {\n"
"    background-color:rgb(233, 233, 233);\n"
"    border-top: 1px solid rgb(70, 70, 70);\n"
"}\n"
"\n"
"QTabBar::tab { \n"
"    max-width: 250px;\n"
"    margin-top: 1px; \n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid black;\n"
"    background: white;\n"
"}\n"
"\n"
"QTabWidget::tab-bar:top {\n"
"    top: 1px;\n"
"}\n"
"\n"
"QTabWidget::tab-bar:bottom {\n"
"    bottom: 1px;\n"
"}\n"
"\n"
"QTabWidget::tab-bar:left {\n"
"    right: 1px;\n"
"}\n"
"\n"
"QTabWidget::tab-bar:right {\n"
"    left: 1px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: white;\n"
"    margin-right: 1px;\n"
"}\n"
"\n"
"QTabBar::tab:selected:!first {\n"
"    margin-left: 1px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    background: rgb(240, 240, 240);\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover {\n"
"    background: rgb(245, 245, 245);\n"
"}\n"
"\n"
"QTabBar::tab:!selected:!previous-selected:middle {\n"
"    border-left: 1px solid rgb(150, 150, 150); \n"
"}\n"
"\n"
"QTabBar::tab:last:!previous-selected {\n"
"    border-left: 1px solid rgb(150, 150, 150); \n"
"}\n"
"\n"
"QTabBar::tab:top:last {\n"
"    margin-right: 0;\n"
"    width: 4ex;\n"
"}\n"
"\n"
"QTabBar::tab:top, QTabBar::tab:bottom {\n"
"\n"
"    padding: 5px 10px 5px 10px;\n"
"}\n"
"\n"
"QTabBar::tab:top:selected {\n"
"    border-bottom-color: none;\n"
"}\n"
"\n"
"QTabBar::close-button {\n"
"    image: url(\"img/close-tab.png\");\n"
"}\n"
"\n"
"QTabBar::close-button:hover {\n"
"    image: url(\"img/close-tab-hover.png\");\n"
"}")
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tabAnadir = QtWidgets.QWidget()
        self.tabAnadir.setObjectName("tabAnadir")
        self.tabWidget.addTab(self.tabAnadir, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionNewTab = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("img/new-tab.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionNewTab.setIcon(icon7)
        self.actionNewTab.setObjectName("actionNewTab")
        self.actionCloseTab = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("img/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCloseTab.setIcon(icon8)
        self.actionCloseTab.setObjectName("actionCloseTab")
        self.actionSalir = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("img/logout.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionSalir.setIcon(icon9)
        self.actionSalir.setObjectName("actionSalir")
        self.actionHistorial = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("img/history.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionHistorial.setIcon(icon10)
        self.actionHistorial.setObjectName("actionHistorial")
        self.actionMostrar_marcadores = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("img/favorite.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.actionMostrar_marcadores.setIcon(icon11)
        self.actionMostrar_marcadores.setObjectName("actionMostrar_marcadores")
        self.actionAdministrar_marcadores = QtWidgets.QAction(MainWindow)
        self.actionAdministrar_marcadores.setObjectName("actionAdministrar_marcadores")
        self.actionAcerca_de = QtWidgets.QAction(MainWindow)
        self.actionAcerca_de.setObjectName("actionAcerca_de")
        self.actionAyuda = QtWidgets.QAction(MainWindow)
        self.actionAyuda.setObjectName("actionAyuda")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAnadir), _translate("MainWindow", "+"))
        self.actionNewTab.setText(_translate("MainWindow", "Nueva pestaña"))
        self.actionNewTab.setToolTip(_translate("MainWindow", "Abrir una nueva pestaña"))
        self.actionNewTab.setShortcut(_translate("MainWindow", "Ctrl+T"))
        self.actionCloseTab.setText(_translate("MainWindow", "Cerrar pestaña"))
        self.actionCloseTab.setToolTip(_translate("MainWindow", "Cierra la pestaña actual"))
        self.actionCloseTab.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionSalir.setText(_translate("MainWindow", "Salir del programa"))
        self.actionSalir.setToolTip(_translate("MainWindow", "Salir del programa"))
        self.actionSalir.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionHistorial.setText(_translate("MainWindow", "Abrir historial"))
        self.actionHistorial.setToolTip(_translate("MainWindow", "Abrir el historial de busqueda"))
        self.actionHistorial.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.actionMostrar_marcadores.setText(_translate("MainWindow", "Mostrar marcadores"))
        self.actionMostrar_marcadores.setToolTip(_translate("MainWindow", "Mostrar o ocultar barra de marcadores"))
        self.actionAdministrar_marcadores.setText(_translate("MainWindow", "Administrar marcadores"))
        self.actionAcerca_de.setText(_translate("MainWindow", "Acerca de"))
        self.actionAyuda.setText(_translate("MainWindow", "Ayuda"))
