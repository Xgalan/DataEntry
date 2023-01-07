# -*- coding: utf-8 -*-
from __future__ import annotations

from data_entry.model import Model
import data_entry.controller as controller
import data_entry.view as view


def main() -> None:
    from tkinter import messagebox

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            app.destroy()


    model = Model()
    app = view.Window()
    tkview = view.MainFrame(master=app)
    ctrller = controller.Controller(model=model, view=tkview)
    ctrller.attach(tkview)
    tkview.controller = ctrller
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()