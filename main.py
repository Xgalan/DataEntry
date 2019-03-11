#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk

from model import Model
from view import Application
from icons import window_image


if __name__ == "__main__":
    root = tk.Tk()
    window_icon = tk.PhotoImage(data=window_image)
    model = Model()
    view = Application(master=root, model=model)
    model.attach(view)
    root.tk.call('wm', 'iconphoto', root._w, window_icon)
    root.title("Data Entry")
    root.mainloop()
