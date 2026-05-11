import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._fermataPartenza = None
        self._fermataArrivo = None


    def handleCreaGrafo(self,e):
        self._model.buildGraph()
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        self._view.lst_result.controls.append(ft.Text(f"il grafo da {self._model.get_numnodi()}"))
        self._view.lst_result.controls.append(ft.Text(f"il grafo da {self._model.get_numarchi()}"))
        self._view.update_page()
        #self._model.b DA AGGIUNGERE

    def handleCercaRaggiungibili(self,e):
        if self._fermataPartenza is None:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text(f"scegliere", color = "red"))
            self._view.update_page()
            return
        nodes = self._model.getBFSNodesFromEdges(self._fermataPartenza)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"i nodi da {self._fermataPartenza}"))
        for n in nodes:
            self._view.lst_result.controls.append(ft.Text(f"{n}"))

        self._view.update_page()

    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def handleTrovaPercorso(self, e):
        if self._fermataPartenza is None or self._fermataArrivo is None:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text(f"Seleziona tutto"), color = "red")

            self._view.update_page()
            return

        totTime, optPath = self._model.getShortestPath(self._fermataPartenza, self._fermataArrivo)

        if optPath == []:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text(f"Cammino non trovato tra {self._fermataPartenza} e {self._fermataArrivo}", color = "orange"))
            return

        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"{totTime}", color = "green"))
        for v in optPath:
            self._view.lst_result.controls.append(ft.Text(f"{v}"))
        self._view.update_page()

    def read_DD_Partenza(self,e):
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data