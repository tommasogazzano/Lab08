import copy
import datetime
from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()



    def worstCase(self, nerc, maxY, maxH):
        self._solBest = []  #inizializzo a 0 la lista delle soluzioni ogni volta che chiamo la funzione

        self.loadEvents(nerc)

        maxYear = int(maxY)
        maxHour = int(maxH)
        self._listEvents = sorted(self._listEvents, key=lambda e: e.customers_affected, reverse=True)

        self.ricorsione([], maxYear, maxHour, 0)
        return self._solBest

    def isBest(self, soluzione1, soluzione2):
        if not soluzione1:
            return False
        if not soluzione2:
            return True

        total_affected1 = sum(event.customers_affected for event in soluzione1)
        total_affected2 = sum(event.customers_affected for event in soluzione2)

        return total_affected1 > total_affected2

    def calcolaOre(self, evento):
        inizio = evento.date_event_began
        fine = evento.date_event_finished

        intervallo = fine - inizio
        oreTot = intervallo.total_seconds()/3600

        return oreTot

    def verificaVincoli(self, parziale, maxY, maxH):
        #vincolo lista di soluzioni parziale --> se è vuota ritorno False
        if len(parziale)==0:
            return True
        #vincolo ore Totali
        oreTot = sum(self.calcolaOre(evento) for evento in parziale)
        if oreTot > maxH:
            return False

        #vincolo anni
        anni = [evento.date_event_began.year for evento in parziale]

        if len(anni) <= 1:
            return True

        annoMax = max(anni)
        annoMin = min(anni)

        if (annoMax - annoMin) > int(maxY):
            return False

        return True

    def ricorsione(self, parziale, maxY, maxH, pos):
        if pos >= len(self._listEvents):
            if self.isBest(parziale, self._solBest):
                self._solBest = copy.deepcopy(parziale)
            return
        else:
            eventoCorrente = self._listEvents[pos]
            nuovoParziale = parziale + [eventoCorrente]

            if self.verificaVincoli(nuovoParziale, maxY, maxH):
                self.ricorsione(nuovoParziale, maxY, maxH, pos +1 )

            self.ricorsione(parziale, maxY, maxH, pos + 1)

            pass

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc