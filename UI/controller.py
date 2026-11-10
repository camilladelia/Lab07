import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.biblioteca_selezionata = None
        self.genere_selezionato = None

    # POPOLA DROPDOWN
    def popola_dropdown(self):
        # 1. popola dropdown delle biblioteche
        self._view.dd_biblioteca.options.clear()
        self._view.dd_biblioteca.options.append(ft.dropdown.Option("Nessun filtro"))

        biblioteche= self._model.get_biblioteche()
        if biblioteche:
            for b in biblioteche:
                #aggiungi il nome di ogni biblioteca al menù
                self._view.dd_biblioteca.options.append(ft.dropdown.Option(b.nome))

        # 2. popola dropdown dei generi
        self._view.dd_genere.options.clear()
        self._view.dd_genere.options.append(ft.dropdown.Option("Nessun filtro"))

        generi= self._model.get_generi()
        if generi:
            for g in generi:
                #aggiungi il nome di ogni genere al menù
                self._view.dd_genere.options.append(ft.dropdown.Option(g))

        self._view.update()

    # CALLBACKS DROPDOWN
    def leggi_biblioteca(self,e):
        valore= self._view.dd_biblioteca.value
        self.biblioteca_selezionata = None if valore == "Nessun filtro" else valore

    def leggi_genere(self,e):
        valore= self._view.dd_genere.value
        self.genere_selezionato= None if valore == "Nessun filtro" else valore

    # AZIONE: MOSTRA LIBRI
    def mostra_libri(self,e):
        self._view.lista_libri.controls.clear()

        libri = self._model.get_libri_filtrati(self.biblioteca_selezionata, self. genere_selezionato)

        if libri is None:
            self._view.show_alert("Errore di connessione al database")
            return

        if len(libri)== 0:
            self._view.show_alert("Nessun libro trovato con i criteri selezionati.")
        else:
            for libro in libri:
                self._view.lista_libri.controls.append(ft.Text(str(libro)))

        self._view.update()