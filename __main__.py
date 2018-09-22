#!/usr/bin/env python3
# coding: utf-8

import tkinter as tk

from model import Model
from view import Application


if __name__ == "__main__":
    root = tk.Tk()    
    app = Application(master=root)
    model = Model(observable=app)
    app.master.title("Data Entry")
    app.mainloop()
