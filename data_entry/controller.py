# -*- coding: utf-8 -*-

import csv
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import NamedStyle, Font, Border, Side
import pygal

from model import Model
from statsutils import Stats



class Controller:
    def __init__(self, view=None):
        self._model = Model()
        self.view = view

    def __getattr__(self, name):
        attr = getattr(self._model, name)

        if not callable(attr):
            return attr

        def wrapper(*args, **kwargs):
            return attr(*args, **kwargs)
        return wrapper

    def set_values(self, values):
        self._model.values = values

    def set_offset(self, offset):
        self._model.offset = offset

    def set_units(self, units):
        self._model.units = units

    def set_precision(self, value):
        self._model.precision = value

    def set_tolerance(self, tolerance):
        self._model.tolerance = tolerance

    @property
    def stats(self):
        return Stats(self.values)

    def export_to_csv(self, filename):
        um = self.units.description
        with open(filename, 'w', newline='') as csvfile:
            exported_file = csv.writer(csvfile, dialect='excel')
            exported_file.writerow(['Value', 'Units'])
            [exported_file.writerow([str(line), um]) for line in
             self.values]

    def export_svg(self, filename):
        um = self.units.description
        # chart creation
        bar_chart = pygal.Bar()
        bar_chart.title = "Samples data (" + um + ")"
        bar_chart.x_labels = map(str, range(1, len(self.values) + 1))
        bar_chart.add("Sample length (" + um + ")", self.values)
        bar_chart.render_to_file(filename)

    def export_xlsx(self, filename):
        um = self.units.description
        data = [(i+1,v,um) for (i,v) in enumerate(self.values)]
        wb = Workbook(write_only = True)
        ws = wb.create_sheet()
        # create some styles
        cellstyle = NamedStyle(name="highlight")
        headerstyle = NamedStyle(name='headercell')
        wb.add_named_style(cellstyle)
        wb.add_named_style(headerstyle)
        cellstyle.font = Font(name='Calibri', size=11)
        headerstyle.font = Font(name='Calibri', size=11, bold=True)
        bd = Side(border_style='thin')
        cellstyle.border = Border(bottom=bd, right=bd, top=bd, left=bd)
        headerstyle.border = Border(bottom=bd, right=bd, top=bd, left=bd)
        header_labels = ['#', 'Value', 'Units']
        # write header
        header = []
        for el in header_labels:
            cell = WriteOnlyCell(ws, value=el)
            cell.style = 'headercell'
            header.append(cell)
        ws.append(header)
        # write data
        for t in data:
            row = []
            for el in t:
                cell = WriteOnlyCell(ws, value=el)
                cell.style = 'highlight'
                row.append(cell)
            ws.append(row)
        wb.save(filename) # doctest: +SKIP
