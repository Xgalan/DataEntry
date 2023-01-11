# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import json
from datetime import date
from typing import Any, Callable

from data_entry.statsutils import Stats
from data_entry.view import MainFrame


class Controller:
    def __init__(self, model=None, view=None) -> None:
        self._model = model
        self.view = view

    def __getattr__(self, name: str) -> Any | Callable:
        attr = getattr(self._model, name)

        if not callable(attr):
            return attr

        def wrapper(*args, **kwargs):
            return attr(*args, **kwargs)

        return wrapper

    def run(self) -> None:
        self.view.main.attach(self)
        self.view.mainloop()

    def update_from_subject(self, subject: MainFrame) -> None:
        """observer pattern"""

        if "text" in subject._vars:
            self._model.values = subject._vars["text"]
        if "precision" in subject._vars:
            self._model.precision = subject._vars["precision"]
        if "offset" in subject._vars:
            self._model.offset = subject._vars["offset"]
        if "units" in subject._vars:
            self._model.units = subject._vars["units"]
        if "tolerance" in subject._vars:
            self._model.tolerance = subject._vars["tolerance"]

        self.view.main.update_from_model(self._model)

        if "filename" in subject._vars:
            filename = subject._vars["filename"]
            if filename.endswith(".csv"):
                self.export_to_csv(filename)
            if filename.endswith(".json"):
                self.export_as_json(filename)

    @property
    def stats(self) -> Stats:
        return Stats(self.values)

    def export_to_csv(self, filename) -> None:
        um = self.units.description
        with open(filename, "w", newline="") as csvfile:
            exported_file = csv.writer(csvfile, dialect="excel")
            exported_file.writerow(["#", "Value", "Units"])
            [
                exported_file.writerow([i + 1, str(line), um])
                for (i, line) in enumerate(self.values)
            ]

    def export_as_json(self, filename) -> None:
        model = {
            "values": self.values,
            "offset": self.offset,
            "tolerance": self.tolerance,
            "measure": {"precision": self.precision, "um": self.units.description},
            "stats": {
                "count": len(self.values),
                "min": self.min(),
                "max": self.max(),
                "min_max": self.min_max(),
                "median": self.stats.median,
            },
            "date": date.isoformat(date.today()),
        }
        with open(filename, "w") as jsonf:
            json.dump(model, jsonf)
