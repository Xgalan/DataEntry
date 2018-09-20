#!/usr/bin/env python3
# coding: utf-8

import tkinter as tk

from model import Model
from view import Application


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.model = Model()
    app.master.title("Min Max measurements")
    app.master.maxsize(270,700)
    app.master.geometry('{}x{}'.format(240, 570))
    app.mainloop()
