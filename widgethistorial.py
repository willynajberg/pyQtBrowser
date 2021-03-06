from datetime import datetime

from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
from PyQt5.QtWidgets import QWidget, QMenu


class WidgetHistorial(QWidget):
    """

    Clase que instancia un QWidget nuevo que contiene la tabla de entradas del historial, y define su comportamiento.

    """
    historialRecibido = QtCore.pyqtSignal(QtSql.QSqlQuery)

    def __init__(self, nav):
        """

        Crea una nueva instancia de la clase. Recibe el objeto de la ventana principal.

        :param nav: Ventana principal
        :type nav: Main
        """
        super(WidgetHistorial, self).__init__()

        self.menu = QMenu(self)
        self.nav = nav
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)

        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)

        # Oculta la columna con índice 4, esta es la columna que contiene el indice de entrada de historial.
        self.tableWidget.hideColumn(4)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setText("Título")
        self.tableWidget.setHorizontalHeaderItem(0, item)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setText("Fecha")
        self.tableWidget.setHorizontalHeaderItem(1, item)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setText("Hora")
        self.tableWidget.setHorizontalHeaderItem(2, item)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setText("URL")
        self.tableWidget.setHorizontalHeaderItem(3, item)

        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.tableWidget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.btnBorrarSel = QtWidgets.QPushButton(self)
        self.horizontalLayout.addWidget(self.btnBorrarSel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.btnBorrarSel.setText("Borrar selección")

        # Gestión de eventos
        self.tableWidget.viewport().installEventFilter(self)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.generar_menu)
        self.btnBorrarSel.clicked.connect(self.borrar_seleccion)

    def eventFilter(self, source, event):
        """

        Se encarga de filtrar los eventos de la tabla de entradas de historial.

        """
        try:
            # Si el evento es un click derecho en la tabla, abre un menú contextual
            if (event.type() == QtCore.QEvent.MouseButtonPress and
                    event.buttons() == QtCore.Qt.RightButton and
                    source is self.tableWidget.viewport()):
                item = self.tableWidget.itemAt(event.pos())

                if item is not None:
                    self.menu = QMenu()
                    self.tableWidget.selectRow(item.row())

                    # Crea los QAction necesarios para gestionar la entrada del historial
                    if self.nav:
                        self.menu.addAction("Ir a sitio", lambda i=item: self.nav.nueva_pestana(
                            self.tableWidget.selectedItems()[3].text()))
                    self.menu.addAction("Borrar entrada", lambda i=item: self.borrar_entrada(
                        int(self.tableWidget.item(i.row().numerator, 4).text())))
        except Exception as error:
            print("Error en event filter de historial: %s" % str(error))
        return super(WidgetHistorial, self).eventFilter(source, event)

    def reload(self):
        """

        Recarga las entradas al historial llamando a la función cargar_historial de la ventana principal.

        """
        self.nav.cargar_historial(self)

    def generar_menu(self, pos):
        """

        Genera un menú contextual en la posición indicada.

        """
        self.menu.exec_(self.tableWidget.mapToGlobal(pos))

    def cargar_historial(self, query):
        """

        Recibe un objeto QSqlQuery que contiene las entradas en el historial y las carga en la tabla iterando este
        objeto.

        :param query: Objeto QSqlQuery que contiene el resultado de la búsqueda.
        :type query: QtSql.QSqlQuery
        """
        try:
            index = 1
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)

            while query.next():
                time = datetime.strptime(query.value(3) + " " + query.value(4), "%d/%m/%Y %H:%M:%S")
                self.tableWidget.setRowCount(index)
                self.tableWidget.setItem(index - 1, 0, QtWidgets.QTableWidgetItem(query.value(2)))
                self.tableWidget.setItem(index - 1, 1, QtWidgets.QTableWidgetItem(time.strftime("%d/%m/%Y")))
                self.tableWidget.setItem(index - 1, 2, QtWidgets.QTableWidgetItem(time.strftime("%H:%M")))
                self.tableWidget.setItem(index - 1, 3, QtWidgets.QTableWidgetItem(query.value(1)))
                self.tableWidget.setItem(index - 1, 4, QtWidgets.QTableWidgetItem(str(query.value(0))))
                index += 1
        except Exception as error:
            print("Error al cargar historial en la pestana: %s" % str(error))

    def borrar_entrada(self, idx=0):
        """

        Función llamada por la QAction de borrar entrada del menú contextual de una entrada en la tabla.
        Llamará a la función de borrar_entrada_historial de la ventana principal.

        :param idx: Indice de la entrada
        :type idx: int
        """
        try:
            if idx > 0:
                self.nav.borrar_entrada_historial(idx, self)
        except Exception as error:
            print("Error al borrar entrada: %s" % str(error))

    def borrar_seleccion(self):
        """

        Función llamada por el botón de borrar seleccion del widget. Recoge todos los items seleccionados en la tabla,
        coge los valores de la columna 4 que contienen el indice de entrada, y llama a la función de
        borrar_entrada_historial de la ventana principal secuencialmente usando el índice.

        """
        try:
            for x in range(0, len(self.tableWidget.selectedItems()), 4):
                self.nav.borrar_entrada_historial(int(self.tableWidget.item(
                    self.tableWidget.selectedItems()[x].row().numerator, 4).text()), self)

        except Exception as error:
            print("Error al borrar seleccion: %s" % str(error))
