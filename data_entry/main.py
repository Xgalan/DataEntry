# -*- coding: utf-8 -*-
import tkinter as tk

from view import MainFrame
from controller import Controller
from icons import window_image



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        window_icon = tk.PhotoImage(data=window_image)
        self.tk.call('wm', 'iconphoto', self._w, window_icon)
        self.title("Data Entry")
        self.resizable(False, False)


if __name__ == "__main__":
    app = App()
    tkview = MainFrame(master=app)
    controller = Controller(view=tkview)
    controller.attach(tkview)
    tkview.controller = controller
    app.mainloop()
