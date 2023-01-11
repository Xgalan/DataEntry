import tkinter as tk
from tkinter import ttk


class EditorFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # self.geometry()
        self.__create_widgets()

    def __create_widgets(self):
        self.tree = ttk.Treeview(
            self, columns=("#1", "#2", "#3"), show="headings", height=20
        )
        # define headings
        self.tree.heading("#1", text="#")
        self.tree.heading("#2", text="Measure")
        self.tree.heading("#3", text="Result")
        self.tree.column("#1", width=24)
        self.tree.column("#2", width=128)
        self.tree.column("#3", width=96)
        self.tree.grid(row=0, column=0, sticky="NSEW")
        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, pady=1, sticky="NS")
