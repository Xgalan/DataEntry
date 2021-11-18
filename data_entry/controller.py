# -*- coding: utf-8 -*-
import csv
import json
from datetime import date

from data_entry.model import Model
from data_entry.statsutils import Stats



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
            exported_file.writerow(['#', 'Value', 'Units'])
            [exported_file.writerow([i+1, str(line), um]) for (i,line) in
             enumerate(self.values)]

    def export_as_json(self, filename):
        model = {
            "values": self.values,
            "offset": self.offset,
            "tolerance": self.tolerance,
            "measure": {
                "precision": self.precision,
                "um": self.units.description
            },
            "stats": {
                "count": len(self.values),
                "min": self.min(),
                "max": self.max(),
                "min_max": self.min_max(),
                "median": self.stats.median
            },
            "date": date.isoformat(date.today())
        }
        with open(filename, 'w') as jsonf:
            json.dump(model, jsonf)
