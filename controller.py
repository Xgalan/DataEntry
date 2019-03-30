# -*- coding: utf-8 -*-

import csv

from tableutils import Table
from statsutils import Stats



class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def get_values(self):
        return self.model.values

    def set_values(self, values):
        self.model.values = values

    def set_offset(self, offset):
        self.model.offset = offset

    def get_units(self):
        return self.model.units

    def set_units(self, units):
        self.model.units = units

    @property
    def stats(self):
        return Stats(self.get_values())

    def export_to_csv(self, filename):
        um = self.get_units().description
        with open(filename, 'w', newline='') as csvfile:
            exported_file = csv.writer(csvfile, dialect='excel')
            exported_file.writerow(['Value', 'Units'])
            [exported_file.writerow([str(line), um]) for line in
             self.get_values()]

    def export_to_html(self):
        um = self.get_units()
        data = self.get_values()
        t = Table(data=[(i,v,str(um)) for (i,v) in enumerate(data)],
                  headers=['#', 'Value', 'Units'])
        return '<hr>' + t.to_html()
