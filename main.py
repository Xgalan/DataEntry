# -*- coding: utf-8 -*-
import tkinter as tk

from model import Model
from view import Application
from controller import Controller
from icons import window_image


if __name__ == "__main__":
    root = tk.Tk()
    window_icon = tk.PhotoImage(data=window_image)
    model = Model()
    tkview = Application(master=root)
    model.attach(tkview)
    controller = Controller(model, tkview)
    tkview.controller = controller
    root.tk.call('wm', 'iconphoto', root._w, window_icon)
    root.title("Data Entry")
    root.mainloop()
