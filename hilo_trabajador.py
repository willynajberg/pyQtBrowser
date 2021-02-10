from PyQt5 import QtCore
from PyQt5.QtCore import QThread

import conexion
import var


class HiloTrabajador(QThread):
    """

    Clase auxiliar que instancia un nuevo hilo que se encargue de ejecutar las operaciones CRUD. Se ejecutarán en un
    hilo separado del hilo principal para optimizar el rendimiento.

    """

    # Creación de pyqtSignals propios de la clase para gestionar eventos.
    historialRecibido = QtCore.pyqtSignal(object)
    favoritoAnadido = QtCore.pyqtSignal(int)
    favoritosRecibidos = QtCore.pyqtSignal(object)
    paginaFavorita = QtCore.pyqtSignal(int)

    def __init__(self):
        """

        Se ejecuta al instanciar la clase. Crea una lista nueva vacía que contendrá las tareas a ejecutar. Asigna el
        valor de running a False.

        """
        super(HiloTrabajador, self).__init__()
        self.running = False
        self.tareas = []

    def run(self):
        """

        Establece una conexión del hilo con la base de datos usando la funcion de conectardb del módulo conexion.
        Asigna el valor de running a true. Crea un bucle que se ejecutará con una frecuencia de 20ms, que ejecutará las
        tareas guardadas en la lista en modo FIFO.

        """
        conexion.conectardb(var.NOMBRE_BD)
        self.running = True

        while self.running:
            for tarea in self.tareas:
                tarea()
                self.tareas.remove(tarea)

            # Ahorra recursos reduciendo la frecuencia con la que se ejecuta el hilo
            self.msleep(20)

    def anadir_tarea(self, tarea):
        """

        Añade una tarea nueva, en forma de lambda, a la cola.

        :param tarea: Función a ejecutar
        :type tarea: lambda
        """
        self.tareas.append(tarea)

        if not self.running:
            self.start()

    @staticmethod
    def anadir_historial(navegador):
        """

        Método auxiliar de la clase para agregar una nueva entrada en la tabla historial de la base de datos, a partir
        del objeto de la página actual que se le pasa en argumentos.

        :param navegador: Objeto de tipo QWebEngineView actual
        :type navegador: QtWebEngineWidgets.QWebEngineView

        Comprobará si lo que debe hacer es introducir una entrada nueva o cambiar el título de una entrada previa.
        """
        no_insertar = (conexion.seleccionar_ultima_url() and str(conexion.seleccionar_ultima_url()) == str(
            navegador.url().toString())) or navegador.url().toString() == "about:blank" or (navegador.url().scheme() !=
                                                                                            "http" and
                                                                                            navegador.url().scheme() !=
                                                                                            "https")

        if not no_insertar:
            conexion.insertar_historial(navegador.url().toString(), navegador.page().title())
        else:
            conexion.cambiar_titulo_historial(var.LAST_INSERT_HISTORIAL, navegador.page().title())

    def cargar_historial(self):
        """

        Método auxiliar que carga todas las entradas de la tabla de historial usando el metodo cargar_historial del
        módulo conexion. El objeto QSqlQuery que este devuelve, lo emite en una señal de historialRecibido, para
        tratarlo posteriormente.

        """
        query = conexion.cargar_historial()

        try:
            self.historialRecibido.emit(query)
        except Exception as error:
            print("Error: %s" % str(error))

    @staticmethod
    def anadir_favorito(pag):
        """

        Método auxiliar que recibe un objeto de tipo QWebEnginePage y lo añade a la tabla de favoritos usando el módulo
        de conexion.

        :param pag: Página a añadir
        :type pag: QtWebEngineWidgets.QWebEnginePage
        """
        conexion.anadir_favorito(pag)

    def editar_favorito(self, idx, titulo, url):
        """

        Método auxiliar para editar una entrada en la tabla de favoritos de la base de datos a partir de los parametros
        indicados. Tras ejecutar la orden, cargará los favoritos nuevamente usando el metodo cargar_favoritos.

        :param idx:
        :param titulo:
        :param url:
        """
        conexion.editar_favorito(idx, titulo, url)
        self.cargar_favoritos()

    def cargar_favoritos(self):
        """

        Método auxiliar que carga todas las entradas de la tabla de favoritos usando el metodo cargar_favoritos del
        módulo conexion. El objeto QSqlQuery que este devuelve, lo emite en una señal de favoritosRecibidos, para
        tratarlo posteriormente.

        """
        query = conexion.cargar_favoritos()

        try:
            self.favoritosRecibidos.emit(query)
        except Exception as error:
            print("Error: %s" % str(error))

    def comprobar_favorito(self, url):
        """

        Método auxiliar que comprueba si la URL indicada en argumentos se encuentra en la tabla de favoritos usando el
        método comprobar_favorito del modulo conexion, el booleano que recibe del método, lo emite usando la señal
        paginaFavorita, para que el resultado sea gestionado como un evento.

        :param url: URL de la página a comprobar.
        :type url: str
        """
        es_fav = conexion.comprobar_favorito(url)
        self.paginaFavorita.emit(es_fav)

    @staticmethod
    def borrar_entrada(idx):
        """

        Método auxiliar que borra una URL del historial usando el módulo conexion-

        :param idx: Índice de la página a borrar
        :type idx: int
        """
        conexion.borrar_entrada_historial(idx)

    def parar(self):
        """

        Tras ejecutar todas las tareas restantes, detendrá la ejecución del bucle estableciendo el valor de running a
        False.

        """
        while len(self.tareas) > 0:
            continue

        self.running = False
