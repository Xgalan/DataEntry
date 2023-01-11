# -*- coding: utf-8 -*-
from __future__ import annotations

from data_entry.controller import Controller
from data_entry.model import Model
from data_entry.view import Window


def main() -> None:
    model = Model()
    view = Window()
    ctrller = Controller(model=model, view=view)
    ctrller.run()


if __name__ == "__main__":
    main()
