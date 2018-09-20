#!/usr/bin/env python3
# coding: utf-8
import csv
import tkinter as tk
from tkinter import messagebox, filedialog

from icons import quit_image, copy_image, save_image


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.quit_icon = tk.PhotoImage(data=quit_image)
        self.copy_icon = tk.PhotoImage(data=copy_image)
        self.save_icon = tk.PhotoImage(data=save_image)
        self.offset_option = tk.BooleanVar()
        self.offset_value = tk.DoubleVar()
        self.min_max_var = tk.StringVar()
        self.grid(row=0, columnspan=3)
        self.create_widgets()

    def alert(self):
        ''' show an alert message if the editor has no content. '''
        try:
            tk.messagebox.showwarning("Missing values", "Please insert some values in the editor.")
        except AttributeError:
            return

    def update_preview(self):
        self.min_max_var.set(str(self.model) + self.um_list.get(tk.ACTIVE))

    def offset_cback(self):
        try:
            # check if the user has entered an offset value
            if self.offset_option.get() is True:
                self.model.offset= self.offset_value.get()
                self.update_preview()
            else:
                self.model.offset= 0
                self.update_preview()
            return self.offset_option.get()
        except ValueError:
            return

    def update_model_values(self, *args):
        text = self.get_editor_content()
        if text is not None:
            self.model.values= text.splitlines()
            self.update_preview()
            return

    def create_widgets(self):
        # menu
        self.menu = tk.Frame(self, padx=2, pady=2, bd=1)
        self.menu.grid(row=0, sticky='NWE')

        # save to CSV button
        self.save_btn = tk.Button(self.menu, command=self.export_as_csv,
                                  image=self.save_icon)
        self.save_btn.image = self.save_icon
        self.save_btn.grid(row=0, column=1, sticky='E')
        # quit button
        self.quit = tk.Button(self.menu, image=self.quit_icon, command=self.master.destroy)
        self.quit.image = self.quit_icon
        self.quit.grid(row=0, column=2, sticky='E')

        # editor
        self.editor = tk.LabelFrame(self, text='Measurements: ')
        self.editor.grid(row=1, padx=4, pady=4, sticky='W')
        # clear text button
        self.data_entry_clear = tk.Button(self.editor, text="Clear",
                                          command=self.clear_data_entry)
        self.data_entry_clear.grid(row=1, column=0, pady=1, sticky='W')
        self.scrollbar = tk.Scrollbar(self.editor)
        self.scrollbar.grid(row=0, column=1, pady=1, sticky="NS")
        self.data_entry = tk.Text(self.editor, width=24,
                                  yscrollcommand=self.scrollbar.set)
        self.data_entry.grid(row=0, column=0, sticky='WE')
        # update event on data entry text widget
        self.data_entry.bind("<Return>", self.update_model_values)
        self.scrollbar.config(command=self.data_entry.yview)
        

        # statistics group frame
        self.stats = tk.LabelFrame(self, text="Stats")
        self.stats.grid(row=3, padx=4, pady=4, sticky='EW')

        # string preview with copy to clipboard button
        self.preview_separator = tk.Frame(self.stats, height=2,
                                          bd=1, relief=tk.SUNKEN)
        self.preview_separator.grid(row=1, columnspan=2,
                                    padx=4, pady=4, sticky='EW')
        self.copy_preview = tk.Entry(self.stats, textvariable=self.min_max_var,
                                     relief=tk.FLAT, state=tk.DISABLED)
        self.copy_preview.grid(row=2, column=0, padx=2)
        self.copy_to_clip_btn = tk.Button(self.stats, command=self.cp_to_clipboard,
                                          image=self.copy_icon)
        self.copy_to_clip_btn.image = self.copy_icon
        self.copy_to_clip_btn.grid(row=2, column=1)

        # options group frame
        self.options = tk.LabelFrame(self, text="Options")
        self.options.grid(row=4, padx=4, pady=4, sticky='EW')

        # measure offset - accepts a positive or negative number
        self.offset_checkbutton = tk.Checkbutton(self.options, text='Offset',
                                                 variable=self.offset_option,
                                                 command=self.offset_cback)
        self.offset_checkbutton.grid(row=0, column=0, pady=2, sticky='W')
        self.offset_entry = tk.Entry(self.options, width=8, textvariable=self.offset_value)
        self.offset_entry.grid(row=0, column=1, padx=1, pady=2, sticky='E')

        # listbox u.m.
        self.um_list_label = tk.Label(self.options, text='Unit of measurement:')
        self.um_list_label.grid(row=1, column=0, pady=2, sticky='NW')
        self.um_list = tk.Listbox(self.options)
        self.um_list.insert('end', "mm")
        self.um_list.config(height=2, width=6)
        self.um_list.grid(row=1, column=1, padx=1, pady=2, sticky='E')

    def get_editor_content(self):
        ''' check if the editor is empty or return the content. '''
        text = self.data_entry.get("1.0",'end-1c')
        if text == '':
            text = None
            self.alert()
            pass
        else:
            return text

    def cp_to_clipboard(self):
        ''' copy to clipboard the converted values from the text editor. '''
        self.clipboard_clear()
        text = self.get_editor_content()
        if text is not None:
            try:
                # check if the user has entered an offset value
                if self.offset_option.get() is True:
                    self.model.offset = self.offset_value.get()
                else:
                    self.model.offset = 0
                # find the min and max values in the collection
                self.model.values= text.splitlines()
                self.clipboard_append(str(self.model) + self.um_list.get(tk.ACTIVE))
            except ValueError:
                return
        self.update()

    def clear_data_entry(self):
        ''' delete the content of the editor and delete the values of the options. '''
        self.data_entry.delete("1.0",'end-1c')
        self.offset_entry.delete(0,tk.END)
        self.offset_checkbutton.deselect()
        self.min_max_var.set('')
        self.update()

    def export_as_csv(self):
        ''' export as a CSV file the content of the editor. '''
        text = self.get_editor_content()
        if text is not None:
            filename = filedialog.asksaveasfilename(initialdir = "/%HOME",
                                                    title = "Export to CSV file",
                                                    filetypes = (("CSV files","*.csv"),("all files","*.*")))
            with open(filename, 'w', newline='') as csvfile:
                exported_file = csv.writer(csvfile, dialect='excel')
                [exported_file.writerow([str(line)]) for line in text.splitlines()]
