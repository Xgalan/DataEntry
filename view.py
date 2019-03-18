#!/usr/bin/env python3
# coding: utf-8

import string
import csv
import tkinter as tk
from tkinter import messagebox, filedialog

import icons
import tooltip
import dialog



class SettingsDialog(dialog.Dialog):
    def body(self, master):
        tk.Label(master, anchor=tk.W, text='Units:').grid(row=0, sticky=tk.W)
        tk.Label(master, anchor=tk.W, text='Precision:').grid(row=1,
                                                              sticky=tk.W)
        tk.Label(master, anchor=tk.W, text='Min. warning:').grid(row=2,
                                                                 sticky=tk.W)
        tk.Label(master, anchor=tk.W, text='Max warning:').grid(row=3,
                                                                sticky=tk.W)
        [setattr(self, 'e' + str(r), tk.Entry(master)) for r in range(1,5)]
        self.e1.insert(0, self.defaults['units'])
        self.e2.insert(0, self.defaults['precision'])
        self.e3.insert(0, self.defaults['min_warning'])
        self.e4.insert(0, self.defaults['max_warning'])
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        return self.e1 # initial focus

    def validate(self):
        if isinstance(self.e1.get(), str) and isinstance(int(self.e2.get()), int):
            return True
        else:
            return False

    def apply(self):
        self.units = self.e1.get()
        self.precision = self.e2.get()
        self.min_warning = self.e3.get()
        self.max_warning = self.e4.get()


class Application(tk.Frame):
    def __init__(self, master=None, model=None):
        super().__init__(master)
        self.model = model
        # icons
        self.quit_icon = tk.PhotoImage(data=icons.quit_image)
        self.copy_icon = tk.PhotoImage(data=icons.copy_image)
        self.save_icon = tk.PhotoImage(data=icons.save_image)
        self.delete_icon = tk.PhotoImage(data=icons.delete_image)
        self.minimize_icon = tk.PhotoImage(data=icons.minimize_image)
        self.options_icon = tk.PhotoImage(data=icons.options_image)
        self.green_icon = tk.PhotoImage(data=icons.green_led)
        self.neutral_icon = tk.PhotoImage(data=icons.neutral_led)
        self.yellow_icon = tk.PhotoImage(data=icons.yellow_led)
        # tk Vars initialization
        self.offset_option = tk.BooleanVar()
        self.min_max_var = tk.StringVar(value='- - - - -')
        self.min_max_var.default = '- - - - -'
        self.count_var = tk.StringVar(value='Count: 0')
        self.mean_var = tk.DoubleVar(0.0)
        self.pstdev_var = tk.DoubleVar(0.0)
        self.precision = tk.IntVar()
        self.precision.set(self.model.units.precision)
        self.min_warning = tk.DoubleVar(0.0)
        self.max_warning = tk.DoubleVar(0.0)
        self.last_value = tk.StringVar(value='- - - - - -')
        # validation callbacks
        self._validate_num = self.register(self.validate_number)
        # create graphics
        self.grid()
        self.create_widgets()

    def quit_dialog(self):
        if self.data_entry.edit_modified() is 1:
            answer = messagebox.askokcancel("Quit","Do you want to quit?")
            if answer:
                self.master.destroy()
        else:
            self.master.destroy()

    def validate_number(self, *args):
        list_of_num = list(string.digits)
        list_of_num.append('.')
        list_of_num.append('-')
        if args[0] in (list_of_num):
            return True
        else:
            return False

    def flasher(self, widget, color):
        ''' Change the background color of a widget for 100ms. '''
        def change_color(widget, color):
            widget.config(bg=color)

        orig_color = widget.cget('bg')
        self.count_label.after(10, change_color, widget, color)
        self.count_label.after(210, change_color, widget, orig_color)

    def alert(self, **kwargs):
        ''' show an alert message if the editor has no content. '''
        try:
            tk.messagebox.showwarning("Missing values", kwargs['msg'])
        except AttributeError:
            return

    def update_values(self, subject):
        ''' observer pattern '''
        precision = subject.units.precision
        units = subject.units.units
        self.count_var.set(subject.count_values())
        self.flasher(self.count_label, 'snow2')
        self.mean_var.set(round(subject.mean(), precision))
        self.pstdev_var.set(round(subject.pstdev(), precision))
        self.min_max_var.set(
            str(round(subject.min(), precision)) + ' - ' + str(
                round(subject.max(), precision)) + ' ' + units)
        try:
            last_val = subject.values[-1]
            self.last_value.set(str(last_val) + ' ' + units)
        except IndexError:
            self.last_value.set('No valid value')

    def offset_cback(self):
        try:
            # check if the user has entered an offset value
            if self.offset_option.get() is True:
                self.model.offset=float(self.offset_entry.get())
            else:
                self.model.offset=0.0
            return self.offset_option.get()
        except ValueError:
            return

    def update_model_values(self, *args):
        text = self.get_editor_content()
        if text is not None:
            self.model.values = text.splitlines()
            lastv = self.model.values[-1]
            if lastv >= self.min_warning.get() and lastv <= self.max_warning.get():
                self.warning_label.configure(image=self.green_icon)
                self.warning_label.image = self.green_icon
            else:
                self.warning_label.configure(image=self.yellow_icon)
                self.warning_label.image = self.yellow_icon

    def settings_dialog(self):
        ''' Open a dialog with choices for unit of measurement '''
        defaults = {
            'units': self.model.units,
            'precision': self.precision.get(),
            'min_warning': self.min_warning.get(),
            'max_warning': self.max_warning.get(),
            }
        self.d = SettingsDialog(self, title='Settings', defaults=defaults)
        if hasattr(self.d, 'units'):
            self.model.units = self.d.units
        if hasattr(self.d, 'precision'):
            self.precision.set(self.d.precision)
        if hasattr(self.d, 'min_warning'):
            self.min_warning.set(self.d.min_warning)
        if hasattr(self.d, 'max_warning'):
            self.max_warning.set(self.d.max_warning)

    def create_widgets(self):
        # menu
        self.menu = tk.Frame(self, padx=2, pady=3, bd=1, relief=tk.RAISED)
        self.menu.grid(row=0, sticky='NWE')
        # quit button
        self.quit = tk.Button(self.menu, image=self.quit_icon,
                              command=self.quit_dialog)
        self.quit.image = self.quit_icon
        self.quit.grid(row=0, column=5, sticky=tk.E)
        # minimize to tray button
        self.minimize = tk.Button(self.menu, image=self.minimize_icon,
                                  command=self.master.wm_iconify)
        self.minimize.image = self.minimize_icon
        self.minimize.grid(row=0, column=4, sticky=tk.E)
        # copy to clipboard
        self.copy_to_clip_btn = tk.Button(self.menu,
                                          command=self.cp_to_clipboard,
                                          image=self.copy_icon)
        self.copy_to_clip_btn.image = self.copy_icon
        self.copy_to_clip_btn.grid(row=0, column=0)
        # save to CSV button
        self.save_btn = tk.Button(self.menu,
                                  command=self.export_as_csv,
                                  image=self.save_icon)
        self.save_btn.image = self.save_icon
        self.save_btn.grid(row=0, column=1, sticky=tk.E)
        # settings button
        self.settings_btn = tk.Button(self.menu,
                                      command=self.settings_dialog,
                                      image=self.options_icon)
        self.settings_btn.image = self.options_icon
        self.settings_btn.grid(row=0, column=3, sticky=tk.E)
        # reset data entry button
        self.data_entry_clear = tk.Button(self.menu,
                                          command=self.clear_data_entry,
                                          image=self.delete_icon)
        self.data_entry_clear.image = self.delete_icon
        self.data_entry_clear.grid(row=0, column=2, sticky=tk.E)
        
        # tooltips
        tooltip.Tooltip(self.quit, text='Quit')
        tooltip.Tooltip(self.minimize, text='Minimize')
        tooltip.Tooltip(self.save_btn, text='Save to CSV...')
        tooltip.Tooltip(self.settings_btn, text='Settings...')
        tooltip.Tooltip(self.copy_to_clip_btn, text='Copy to clipboard')
        tooltip.Tooltip(self.data_entry_clear, text='Reset')
        # editor
        self.editor = tk.Frame(self, bd=1, relief=tk.FLAT)
        self.editor.grid(row=1, padx=2, pady=2, sticky=tk.W+tk.E)
        self.scrollbar = tk.Scrollbar(self.editor)
        self.scrollbar.grid(row=0, column=1, pady=1, sticky="NS")
        self.data_entry = tk.Text(self.editor, width=22,
                                  yscrollcommand=self.scrollbar.set)
        self.data_entry.grid(row=0, column=0, sticky=tk.W+tk.E)
        # update event on data entry text widget
        self.data_entry.bind("<Return>", self.update_model_values)
        self.scrollbar.config(command=self.data_entry.yview)
        # editor menu frame
        self.editor_menu = tk.Frame(self.editor)
        self.editor_menu.grid(row=1, columnspan=3, pady=2, sticky=tk.W+tk.E)

        # model elements count
        self.count_label = tk.Label(self.editor_menu, bg='white',
                                    width=16, bd=1, relief=tk.SUNKEN,
                                    font=("Helvetica", 10, "bold"),
                                    textvariable=self.count_var)
        self.count_label.grid(row=0, column=0, padx=2, pady=1)
        # good/warning icon
        self.warning_label = tk.Label(self.editor_menu,
                                      image=self.neutral_icon)
        self.warning_label.grid(row=0, rowspan=2, column=2, padx=6)
        self.last_value_with_offset = tk.Label(self.editor_menu, bg='white',
                                               width=16, bd=1, relief=tk.SUNKEN,
                                               font=("Helvetica", 10, "bold"),
                                               textvariable=self.last_value)
        self.last_value_with_offset.grid(row=1, padx=2, pady=1, sticky=tk.W)
        # min - max values
        self.copy_preview = tk.Label(self.editor_menu,
                                     textvariable=self.min_max_var, bg='white',
                                     font=("Helvetica", 10, "bold"), bd=1,
                                     relief=tk.SUNKEN)
        self.copy_preview.grid(row=2, columnspan=2, padx=2, pady=1,
                               sticky=tk.W+tk.E)
        # statistics group frame
        self.stats = tk.LabelFrame(self, text="Statistics",
                                   font=("Helvetica", 9))
        self.stats.grid(row=3, padx=4, pady=3, sticky=tk.W+tk.E)
        self.mean_label = tk.Label(self.stats, text='Mean',
                                   anchor=tk.W, font=("Helvetica", 9, "bold"))
        self.mean_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
        self.pstdev_label = tk.Label(self.stats, text='PopStdDev',
                                     anchor=tk.W, font=("Helvetica", 9, "bold"))
        self.pstdev_label.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)
        self.mean = tk.Label(self.stats, textvariable=self.mean_var,
                             anchor=tk.W, font=("Helvetica", 9))
        self.mean.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
        self.pstdev = tk.Label(self.stats, textvariable=self.pstdev_var,
                               anchor=tk.W, font=("Helvetica", 9))
        self.pstdev.grid(row=1, column=1, padx=2, pady=2, sticky=tk.W)

        # options group frame
        self.options = tk.LabelFrame(self, text="Options",
                                     font=("Helvetica", 9))
        self.options.grid(row=4, padx=4, pady=4, sticky=tk.W+tk.E)
        # measure offset - accepts a positive or negative number
        self.offset_checkbutton = tk.Checkbutton(self.options, text='Offset',
                                                 variable=self.offset_option,
                                                 command=self.offset_cback)
        self.offset_checkbutton.grid(row=0, column=0, pady=2, sticky=tk.W)
        # offset entry with validation
        self.change_sign = tk.Button(self.options, text='+/-',
                                     font=("Helvetica", 9, "bold"),
                                     command=self.change_value_sign)
        self.change_sign.grid(row=0, column=1, padx=1, pady=2, sticky=tk.E)
        tooltip.Tooltip(self.change_sign, text='Change offset sign')
        self.offset_entry = tk.Entry(self.options, width=8,
                                     font=("Helvetica", 10),
                                     validate='key',
                                     validatecommand=(self._validate_num,
                                                      '%S', '%P'))
        self.offset_entry.grid(row=0, column=2, padx=1, pady=2, sticky=tk.E)

        # window resizing
        self.grid_columnconfigure(0, weight=1)
        self.master.resizable(False, False)
        self.update()

    def get_editor_content(self):
        ''' check if the editor is empty or return the content. '''
        text = self.data_entry.get("1.0", 'end-1c')
        if text == '':
            text = None
            self.alert(msg="Please insert some values in the editor.")
            pass
        else:
            return text

    def change_value_sign(self):
        offset_val = self.offset_entry.get()
        if offset_val.find('-', 0, 1) != -1:
            self.offset_entry.delete(0, 1)
            self.offset_checkbutton.deselect()
        else:
            self.offset_entry.insert(0, '-')
            self.offset_checkbutton.deselect()

    def cp_to_clipboard(self):
        '''
        copy to clipboard the converted values from the text editor.
        '''
        self.clipboard_clear()
        text = self.get_editor_content()
        if text is not None:
            self.clipboard_append(
                self.min_max_var.get() + self.model.units.units)
        self.update()

    def clear_data_entry(self):
        '''
        delete the content of the editor and delete the values of the options.
        '''
        self.data_entry.delete("1.0", 'end-1c')
        self.offset_entry.delete(0, tk.END)
        self.offset_checkbutton.deselect()
        self.min_max_var.set(self.min_max_var.default)
        self.count_var.set('Count: 0')
        self.warning_label.configure(image=self.neutral_icon)
        self.warning_label.image = self.neutral_icon
        self.model.values = []
        self.model.offset = 0.0
        self.update()

    def export_as_csv(self):
        ''' export as a CSV file the content of the editor. '''
        text = self.get_editor_content()
        um = self.model.units.description
        if text is not None:
            filename = filedialog.asksaveasfilename(initialdir="/%HOME",
                                                    title="Export to CSV file",
                                                    filetypes=(("CSV files", "*.csv"),
                                                               ("all files", "*.*")))
            with open(filename, 'w', newline='') as csvfile:
                exported_file = csv.writer(csvfile, dialect='excel')
                exported_file.writerow(['Value', 'Units'])
                [exported_file.writerow([str(line), um]) for line in
                 text.splitlines()]
