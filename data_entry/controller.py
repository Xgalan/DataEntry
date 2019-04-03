# -*- coding: utf-8 -*-

import csv
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import NamedStyle, Font, Border, Side

from model import Model
from tableutils import Table
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

    def export_to_html(self):
        um = self.units.description
        tabledata = Table(data=[(i,v,um) for (i,v) in enumerate(self.values)],
                          headers=['#', 'Value', 'Units'])
        statstable = Table(data=self.stats.describe(format='list'),
                           headers=['Property', 'Value'])
        return tabledata.to_html() + '<hr>' + statstable.to_html()

    def export_xlsx(self, filename):
        um = self.units.description
        data = [(i,v,um) for (i,v) in enumerate(self.values)]
        wb = Workbook(write_only = True)
        ws = wb.create_sheet()
        cellstyle = NamedStyle(name="highlight")
        headerstyle = NamedStyle(name='headercell')
        wb.add_named_style(cellstyle)
        wb.add_named_style(headerstyle)
        cellstyle.font = Font(name='Calibri', size=11)
        headerstyle.font = Font(name='Calibri', size=11, bold=True)
        bd = Side(border_style='thin')
        cellstyle.border, headerstyle.border = Border(bottom=bd, right=bd, top=bd, left=bd)
        header_labels = ['#', 'Value', 'Units']
        header = []
        for el in header_labels:
            cell = WriteOnlyCell(ws, value=el)
            cell.style = 'headercell'
            header.append(cell)
        ws.append(header)
        for t in data:
            row = []
            for el in t:
                cell = WriteOnlyCell(ws, value=el)
                cell.style = 'highlight'
                row.append(cell)
            ws.append(row)
        wb.save(filename) # doctest: +SKIP
