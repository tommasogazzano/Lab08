import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        nercID = self._view._ddNerc.value
        maxY = self._view._txtYears.value
        maxH = self._view._txtHours.value

        nerc = self._idMap[nercID]

        self._view._txtOut.controls.clear()

        sol = self._model.worstCase(nerc, maxY, maxH)
        if not sol:
            self._view._txtOut.controls.append(ft.Text("nessun evento trovato"))
        else:
            total_affected = sum(event.customers_affected for event in sol)
            total_hours = sum(self._model.calcolaOre(event) for event in sol)

            self._view._txtOut.controls.append(
                ft.Text(f"Tot people affected: {total_affected}")
            )
            self._view._txtOut.controls.append(
                ft.Text(f"Tot hours of outage: {total_hours:.2f}")
            )

            self._view._txtOut.controls.append(ft.Text(""))

            for event in sol:
                self._view._txtOut.controls.append(ft.Text(event.__str__()))
        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
