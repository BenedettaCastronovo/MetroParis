from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()

    def buildGraph(self):
        pass

    @property
    def fermate(self):
        return self._fermate