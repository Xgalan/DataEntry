# -*- coding: utf-8 -*-
import string
import lzma
import base64
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser

import icons
import tooltip
import dialog



class SettingsDialog(dialog.Dialog):
    def body(self, master):
        tk.Label(master, anchor=tk.W, text='Units').grid(
                     row=0, sticky=tk.W)
        tk.Label(master, anchor=tk.W, text='Precision').grid(
                     row=1, sticky=tk.W)
        tk.Label(master, anchor=tk.W,
                 text='Min. warning').grid(
                     row=2, sticky=tk.W)
        tk.Label(master, anchor=tk.W,
                 text='Max. warning').grid(
                     row=3, sticky=tk.W)
        [setattr(self, 'e' + str(r), tk.Entry(master)) for r in range(1,5)]
        self.e1.insert(0, self.options['units'])
        self.e2.insert(0, self.options['precision'])
        self.e3.insert(0, self.options['min_warning'])
        self.e4.insert(0, self.options['max_warning'])
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        #tooltips
        tooltip.Tooltip(self.e1, text='Enter unit of measurement')
        tooltip.Tooltip(self.e2, text='Enter decimals')
        tooltip.Tooltip(self.e3, text='Enter lower tolerance')
        tooltip.Tooltip(self.e4, text='Enter upper tolerance')
        return self.e1 # initial focus

    def validate(self):
        if isinstance(self.e1.get(), str) and isinstance(int(self.e2.get()), int):
            return True
        else:
            return False

    def apply(self):
        self.settings = {
            'units': self.e1.get(),
            'precision': self.e2.get(),
            'min_warning': self.e3.get(),
            'max_warning': self.e4.get()
            }


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
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
        self.alert_icon = tk.PhotoImage(data=icons.alert_triangle)
        self.chart_icon = tk.PhotoImage(data=icons.bar_chart)
        # tk Vars initialization
        self.offset_option = tk.BooleanVar()
        self.min_max_var = tk.StringVar(value='- - - - - -')
        self.min_max_var.default = '- - - - - -'
        self.count_var = tk.StringVar(value='Count: 0')
        self.precision = tk.IntVar()
        self.precision.set(2)
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
        self.count_var.set(subject.count_values())
        self.flasher(self.count_label, 'snow2')
        self.min_max_var.set(subject.min_max())
        try:
            last_val = round(subject.values[-1], subject.units.precision)
            self.last_value.set(str(last_val) + ' ' + subject.units.units)
        except IndexError:
            self.last_value.set('No valid value')

    def offset_cback(self):
        try:
            # check if the user has entered an offset value
            if self.offset_option.get() is True:
                self.controller.set_offset(float(self.offset_entry.get()))
            else:
                self.controller.offset = 0.0
            return self.offset_option.get()
        except ValueError:
            return

    def update_model_values(self, *args):
        text = self.get_editor_content()
        if text is not None:
            self.controller.set_values(text.splitlines())
            lastv = self.controller.values[-1]
            min_v = self.min_warning.get()
            max_v = self.max_warning.get()
            if lastv >= min_v and lastv <= max_v:
                self.warning_label.configure(image=self.green_icon)
                self.warning_label.image = self.green_icon
            else:
                self.warning_label.configure(image=self.yellow_icon)
                self.warning_label.image = self.yellow_icon
            if self.controller.stats.min < min_v or self.controller.stats.max > max_v:
                self.alert_on_interval.configure(image=self.yellow_icon)
                self.alert_on_interval.image = self.yellow_icon
            else:
                self.alert_on_interval.configure(image=self.green_icon)
                self.alert_on_interval.image = self.green_icon

    def settings_dialog(self):
        ''' Open a dialog with choices for unit of measurement '''
        defaults = {
            'units': self.controller.units,
            'precision': self.precision.get(),
            'min_warning': self.min_warning.get(),
            'max_warning': self.max_warning.get(),
            }
        self.d = SettingsDialog(self, title='Settings', options=defaults)
        if hasattr(self.d, 'settings'):
            self.controller.set_units = self.d.settings['units']
            self.precision.set(self.d.settings['precision'])
            self.min_warning.set(self.d.settings['min_warning'])
            self.max_warning.set(self.d.settings['max_warning'])

    def create_widgets(self):
        # menu
        self.menu = tk.Frame(self, padx=2, pady=3, bd=1, relief=tk.RAISED)
        self.menu.grid(row=0, sticky='NWE')
        # button for statistics dialog
        self.stats_btn = tk.Button(self.menu, image=self.chart_icon,
                                   command=self.export_as_xlsx)
        self.stats_btn.image = self.chart_icon
        self.stats_btn.grid(row=1, column=0, sticky=tk.E)
        # copy to clipboard
        self.copy_to_clip_btn = tk.Button(self.menu,
                                          command=self.cp_to_clipboard,
                                          image=self.copy_icon)
        self.copy_to_clip_btn.image = self.copy_icon
        self.copy_to_clip_btn.grid(row=1, column=1)
        # save to CSV button
        self.save_btn = tk.Button(self.menu,
                                  command=self.export_as_csv,
                                  image=self.save_icon)
        self.save_btn.image = self.save_icon
        self.save_btn.grid(row=1, column=2, sticky=tk.E)
        # reset data entry button
        self.data_entry_clear = tk.Button(self.menu,
                                          command=self.clear_data_entry,
                                          image=self.delete_icon)
        self.data_entry_clear.image = self.delete_icon
        self.data_entry_clear.grid(row=1, column=3, sticky=tk.E)
        # settings button
        self.settings_btn = tk.Button(self.menu,
                                      command=self.settings_dialog,
                                      image=self.options_icon)
        self.settings_btn.image = self.options_icon
        self.settings_btn.grid(row=1, column=4, sticky=tk.E)
        # quit button
        self.quit = tk.Button(self.menu, image=self.quit_icon,
                              command=self.quit_dialog)
        self.quit.image = self.quit_icon
        self.quit.grid(row=0, column=4, sticky=tk.E)
        # minimize to tray button
        self.minimize = tk.Button(self.menu, image=self.minimize_icon,
                                  command=self.master.wm_iconify)
        self.minimize.image = self.minimize_icon
        self.minimize.grid(row=0, column=3, sticky=tk.E)
        # tooltips
        tooltip.Tooltip(self.quit, text='Quit')
        tooltip.Tooltip(self.minimize, text='Minimize')
        tooltip.Tooltip(self.stats_btn, text='View offline statistics...')
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
                                    font=("Helvetica", 11, "bold"),
                                    textvariable=self.count_var)
        self.count_label.grid(row=0, column=0, padx=1, pady=1)
        # good/warning icon
        self.warning_label = tk.Label(self.editor_menu,
                                      image=self.neutral_icon)
        self.warning_label.grid(row=1, column=2, padx=4)
        self.last_value_with_offset = tk.Label(self.editor_menu, bg='white',
                                               width=16, bd=1, relief=tk.SUNKEN,
                                               font=("Helvetica", 11, "bold"),
                                               textvariable=self.last_value)
        self.last_value_with_offset.grid(row=1, padx=1, pady=1, sticky=tk.W)
        tooltip.Tooltip(self.last_value_with_offset, text='Last value')
        # min - max values
        self.copy_preview = tk.Label(self.editor_menu,
                                     textvariable=self.min_max_var, bg='white',
                                     font=("Helvetica", 11, "bold"), bd=1,
                                     relief=tk.SUNKEN)
        self.copy_preview.grid(row=2, columnspan=2, padx=1, pady=2,
                               sticky=tk.W+tk.E)
        tooltip.Tooltip(self.copy_preview, text='Min - Max interval')
        self.alert_on_interval = tk.Label(self.editor_menu,
                                          image=self.neutral_icon)
        self.alert_on_interval.grid(row=2, column=2, padx=4)
        # options group frame
        self.options = tk.LabelFrame(self, text="Options",
                                     font=("Helvetica", 9))
        self.options.grid(row=3, padx=4, pady=4, sticky=tk.W+tk.E)
        # measure offset - accepts a positive or negative number
        self.offset_checkbutton = tk.Checkbutton(self.options, text='Offset',
                                                 variable=self.offset_option,
                                                 command=self.offset_cback)
        self.offset_checkbutton.grid(row=0, pady=2, sticky=tk.W)
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
            self.clipboard_append(self.min_max_var.get())
        self.update()

    def clear_data_entry(self):
        '''
        delete the content of the editor and delete the values of the options.
        '''
        self.data_entry.delete("1.0", 'end-1c')
        self.data_entry.edit_modified(False)
        self.offset_entry.delete(0, tk.END)
        self.offset_checkbutton.deselect()
        self.min_max_var.set(self.min_max_var.default)
        self.count_var.set('Count: 0')
        self.warning_label.configure(image=self.neutral_icon)
        self.warning_label.image = self.neutral_icon
        self.alert_on_interval.configure(image=self.neutral_icon)
        self.alert_on_interval.image = self.neutral_icon
        self.controller.set_values([])
        self.controller.set_offset(0.0)
        self.update()

    def export_as_csv(self):
        ''' export as a CSV file the content of the editor. '''
        text = self.get_editor_content()
        #TODO: check if 'offset' is selected
        if text is not None:
            filename = filedialog.asksaveasfilename(initialdir="/%HOME",
                                                    title="Export to CSV file",
                                                    filetypes=(("CSV files", "*.csv"),
                                                               ("all files", "*.*")))
            self.controller.export_to_csv(filename)
    
    def export_as_xlsx(self):
        ''' export as xlsx file '''
        if self.controller.values:
            filename = filedialog.asksaveasfilename(initialdir="/%HOME",
                                                    title="Export to XLSX file",
                                                    filetypes=(("XLSX files", "*.xlsx"),
                                                               ("all files", "*.*")))
            self.controller.export_xlsx(filename)

    def view_stats(self):
        ''' View offline statistics '''
        url = 'https://itty.bitty.site/#/'+base64.b64encode(
            lzma.compress(
                bytes(self.controller.export_to_html(), encoding="utf-8"),
                format=lzma.FORMAT_ALONE, preset=9)).decode("utf-8")
        webbrowser.open(url, new=2)
