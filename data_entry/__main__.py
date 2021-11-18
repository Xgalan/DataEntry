# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

from view import MainFrame
from controller import Controller
from icons import window_image



class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        window_icon = tk.PhotoImage(data=window_image)
        self.tk.call('wm', 'iconphoto', self._w, window_icon)
        self.title("Data Entry")
        self.resizable(False, False)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        app.destroy()

def init():
    app = App()
    tkview = MainFrame(master=app)
    controller = Controller(view=tkview)
    controller.attach(tkview)
    tkview.controller = controller
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()

if __name__ == "__main__":
    init()