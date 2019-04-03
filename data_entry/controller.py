# -*- coding: utf-8 -*-

import csv
from openpyxl import Workbook

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
    
    def export_xlsx(self):
        um = self.units.description
        table = [[str(line), um] for line in self.values]
        wb = Workbook(write_only = True)
        ws = wb.create_sheet()
        ws.append(table)
        return wb
