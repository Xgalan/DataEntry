# -*- coding: utf-8 -*-
import tkinter as tk

import data_entry.view as view
import data_entry.controller as controller


def init():
    from tkinter import messagebox

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            app.destroy()


    app = App()
    tkview = view.MainFrame(master=app)
    ctrller = controller.Controller(view=tkview)
    ctrller.attach(tkview)
    tkview.controller = ctrller
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        import data_entry.icons as icons
        window_icon = tk.PhotoImage(data=icons.window_image)
        self.tk.call('wm', 'iconphoto', self._w, window_icon)
        self.title("Data Entry")
        self.resizable(False, False)
