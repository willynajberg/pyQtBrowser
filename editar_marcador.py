# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editar_marcador.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlgEditMarcador(object):
    def setupUi(self, dlgEditMarcador):
        dlgEditMarcador.setObjectName("dlgEditMarcador")
        dlgEditMarcador.setWindowModality(QtCore.Qt.ApplicationModal)
        dlgEditMarcador.resize(320, 97)
        dlgEditMarcador.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(dlgEditMarcador)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblTitulo = QtWidgets.QLabel(dlgEditMarcador)
        self.lblTitulo.setObjectName("lblTitulo")
        self.horizontalLayout.addWidget(self.lblTitulo)
        self.txtTitulo = QtWidgets.QLineEdit(dlgEditMarcador)
        self.txtTitulo.setObjectName("txtTitulo")
        self.horizontalLayout.addWidget(self.txtTitulo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblURL = QtWidgets.QLabel(dlgEditMarcador)
        self.lblURL.setObjectName("lblURL")
        self.horizontalLayout_2.addWidget(self.lblURL)
        self.txtURL = QtWidgets.QLineEdit(dlgEditMarcador)
        self.txtURL.setObjectName("txtURL")
        self.horizontalLayout_2.addWidget(self.txtURL)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgEditMarcador)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dlgEditMarcador)
        self.buttonBox.accepted.connect(dlgEditMarcador.accept)
        self.buttonBox.rejected.connect(dlgEditMarcador.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgEditMarcador)

    def retranslateUi(self, dlgEditMarcador):
        _translate = QtCore.QCoreApplication.translate
        dlgEditMarcador.setWindowTitle(_translate("dlgEditMarcador", "Editar marcador"))
        self.lblTitulo.setText(_translate("dlgEditMarcador", "Título:"))
        self.txtTitulo.setPlaceholderText(_translate("dlgEditMarcador", "Título del marcador"))
        self.lblURL.setText(_translate("dlgEditMarcador", "URL:"))
        self.txtURL.setPlaceholderText(_translate("dlgEditMarcador", "URL del marcador"))
