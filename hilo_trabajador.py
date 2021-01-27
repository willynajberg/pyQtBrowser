from PyQt5 import QtCore
from PyQt5.QtCore import QThread

import conexion
import var


# Esta es una clase auxiliar para crear un hilo que se encargue del CRUD
# Este se ejecutará en un hilo separado del hilo principal para optimizar el rendimiento
class HiloTrabajador(QThread):
    historialRecibido = QtCore.pyqtSignal(object)
    favoritoAnadido = QtCore.pyqtSignal(int)
    favoritosRecibidos = QtCore.pyqtSignal(object)
    paginaFavorita = QtCore.pyqtSignal(bool)

    def __init__(self):
        super(HiloTrabajador, self).__init__()
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
        no_insertar = (conexion.seleccionar_ultima_url() and str(conexion.seleccionar_ultima_url()) == str(
            navegador.url().toString())) or navegador.url().toString() == "about:blank"

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

    def anadir_favorito(self, pag):
        idEntrada = conexion.anadir_favorito(pag)

    def editar_favorito(self, idx, titulo, url):
        conexion.editar_favorito(idx, titulo, url)
        self.cargar_favoritos()

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