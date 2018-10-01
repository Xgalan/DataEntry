#!/usr/bin/env python3
# coding: utf-8

import tkinter as tk

from model import Model
from view import Application
from icons import window_image


if __name__ == "__main__":
    root = tk.Tk()
    window_icon = tk.PhotoImage(data=window_image)
    app = Application(master=root)
    model = Model(observable=app)
    root.tk.call('wm', 'iconphoto', root._w, window_icon)
    app.master.title("Data Entry")
    app.mainloop()
