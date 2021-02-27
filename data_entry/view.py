# -*- coding: utf-8 -*-
import string
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

import icons
import tooltip
import dialog
from tabular_editor import EditorFrame



class SettingsDialog(dialog.Dialog):
    def body(self, master):
        ttk.Label(master, anchor=tk.W, text='Units').grid(row=0, sticky=tk.W)
        ttk.Label(master, anchor=tk.W, text='Precision').grid(row=1, sticky=tk.W)
        ttk.Label(master, anchor=tk.W,
                  text='Min. tolerance').grid(row=2, sticky=tk.W)
        ttk.Label(master, anchor=tk.W,
                  text='Max. tolerance').grid(row=3, sticky=tk.W)
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


class MenuFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # icons
        self.quit_icon = tk.PhotoImage(data=icons.quit_image)
        self.copy_icon = tk.PhotoImage(data=icons.copy_image)
        self.save_icon = tk.PhotoImage(data=icons.save_image)
        self.delete_icon = tk.PhotoImage(data=icons.delete_image)
        self.options_icon = tk.PhotoImage(data=icons.options_image)
        self.chart_icon = tk.PhotoImage(data=icons.bar_chart)
        # setup the grid layout manager
        self.columnconfigure(5, weight=1)
        self.__create_widgets()

    def __create_widgets(self):
        # button for statistics dialog
        self.stats_btn = ttk.Button(self, image=self.chart_icon,
                                    command=self.master.view_stats)
        self.stats_btn.image = self.chart_icon
        self.stats_btn.grid(row=0, column=0, sticky=tk.E)
        # copy to clipboard
        self.copy_to_clip_btn = ttk.Button(self,
                                           command=self.master.cp_to_clipboard,
                                           image=self.copy_icon)
        self.copy_to_clip_btn.image = self.copy_icon
        self.copy_to_clip_btn.grid(row=0, column=1)
        # save to file button
        self.save_btn = ttk.Button(self,
                                   command=self.master.export_as,
                                   image=self.save_icon)
        self.save_btn.image = self.save_icon
        self.save_btn.grid(row=0, column=2, sticky=tk.E)
        # reset data entry button
        self.data_entry_clear = ttk.Button(self,
                                           command=self.master.clear_data_entry,
                                           image=self.delete_icon)
        self.data_entry_clear.image = self.delete_icon
        self.data_entry_clear.grid(row=0, column=3, sticky=tk.E)
        # settings button
        self.settings_btn = ttk.Button(self,
                                       command=self.master.settings_dialog,
                                       image=self.options_icon)
        self.settings_btn.image = self.options_icon
        self.settings_btn.grid(row=0, column=4, sticky=tk.E)
        # quit button
        self.quit = ttk.Button(self, image=self.quit_icon,
                               command=self.master.quit_dialog)
        self.quit.image = self.quit_icon
        self.quit.grid(row=0, column=5, sticky=tk.E)
        # tooltips
        tooltip.Tooltip(self.quit, text='Quit')
        tooltip.Tooltip(self.stats_btn, text='View offline statistics...')
        tooltip.Tooltip(self.save_btn, text='Save as...')
        tooltip.Tooltip(self.settings_btn, text='Settings...')
        tooltip.Tooltip(self.copy_to_clip_btn, text='Copy to clipboard')
        tooltip.Tooltip(self.data_entry_clear, text='Reset')


class MainFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.green_icon = tk.PhotoImage(data=icons.green_led)
        self.neutral_icon = tk.PhotoImage(data=icons.neutral_led)
        self.yellow_icon = tk.PhotoImage(data=icons.yellow_led)
        self.alert_icon = tk.PhotoImage(data=icons.alert_triangle)
        # tk Vars initialization
        self.offset_option = tk.BooleanVar()
        self.min_max_var = tk.StringVar(value='- - - - - -')
        self.min_max_var.default = '- - - - - -'
        self.count_var = tk.StringVar(value='Count: 0')
        self.min_warning = tk.DoubleVar(0.0)
        self.max_warning = tk.DoubleVar(0.0)
        self.last_value = tk.StringVar(value='- - - - - -')
        # validation callbacks
        self._validate_num = self.register(self.validate_number)
        # create graphics
        self.grid_columnconfigure(0, weight=1)
        self.grid()
        self.__create_widgets()

    def quit_dialog(self):
        if self.data_entry.edit_modified() == 1:
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
            widget.config(background=color)

        orig_color = widget.cget('background')
        self.count_label.after(10, change_color, widget, color)
        self.count_label.after(210, change_color, widget, orig_color)

    def alert(self, **kwargs):
        ''' show an alert message if the editor has no content. '''
        try:
            tk.messagebox.showwarning("Missing values", kwargs['msg'])
        except AttributeError:
            return

    def update_from_subject(self, subject):
        ''' observer pattern '''
        self.count_var.set(subject.count_values())
        self.flasher(self.count_label, 'snow2')
        self.min_max_var.set(subject.min_max())
        min_v = subject.tolerance['min']
        max_v = subject.tolerance['max']
        try:
            #TODO case if first value is zero i.e., "0.00"
            last_val = round(subject.values[-1], subject.precision)
            self.last_value.set(str(last_val) + ' ' + subject.units.units)
            if last_val >= min_v and last_val <= max_v:
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

    def settings_dialog(self):
        ''' Open a dialog with choices for unit of measurement '''
        defaults = {
            'units': self.controller.units,
            'precision': self.controller.precision,
            'min_warning': self.controller.tolerance['min'],
            'max_warning': self.controller.tolerance['max'],
            }
        self.d = SettingsDialog(self, title='Settings', options=defaults)
        if hasattr(self.d, 'settings'):
            self.controller.set_units(self.d.settings['units'])
            self.controller.set_precision(int(self.d.settings['precision']))
            self.controller.set_tolerance(
                {'min': float(self.d.settings['min_warning']),
                 'max': float(self.d.settings['max_warning'])
                 })

    def __create_widgets(self):
        # menu
        self.menu = MenuFrame(self)
        self.menu['padding'] = (1, 2)
        self.menu['borderwidth'] = 5
        self.menu['relief'] = tk.RAISED
        self.menu.grid(row=0, sticky='NWE')
        
        # editor
        self.editor = ttk.Frame(self)
        self.editor['borderwidth'] = 1
        self.editor['relief'] = tk.FLAT
        self.editor.grid(row=1, sticky=tk.W+tk.E)
        self.scrollbar = ttk.Scrollbar(self.editor)
        self.scrollbar.grid(row=0, column=1, pady=1, sticky="NS")
        self.data_entry = tk.Text(self.editor, width=24,
                                  yscrollcommand=self.scrollbar.set)
        self.data_entry.grid(row=0, column=0, sticky=tk.W+tk.E)
        # update event on data entry text widget
        self.data_entry.bind("<Return>", self.update_model_values)
        self.scrollbar.config(command=self.data_entry.yview)
        # model elements count
        self.count_label = ttk.Label(self.editor, background='white',
                                     borderwidth=1, relief=tk.SUNKEN,
                                     font=("Helvetica", 11, "bold"),
                                     padding=(2, 2),
                                     textvariable=self.count_var)
        self.count_label.grid(row=1, column=0, padx=3, pady=2, sticky=tk.W+tk.E)

        # measures frame
        self.editor_menu = ttk.Frame(self)
        self.editor_menu.columnconfigure(0, weight=2)
        self.editor_menu.columnconfigure(1, weight=1)
        self.editor_menu.grid(row=2, column=0, sticky=tk.W+tk.E)
        # good/warning icon
        self.warning_label = ttk.Label(self.editor_menu,
                                       image=self.neutral_icon)
        self.warning_label.grid(row=0, column=1, padx=4)
        self.last_value_with_offset = ttk.Label(self.editor_menu, background='white',
                                                width=16, borderwidth=1, relief=tk.SUNKEN,
                                                font=("Helvetica", 11, "bold"),
                                                padding=(2, 2),
                                                textvariable=self.last_value)
        self.last_value_with_offset.grid(row=0, column=0, padx=4, sticky=tk.W+tk.E)
        tooltip.Tooltip(self.last_value_with_offset, text='Last value')
        # min - max values
        self.copy_preview = ttk.Label(self.editor_menu,
                                      textvariable=self.min_max_var, background='white',
                                      font=("Helvetica", 11, "bold"), borderwidth=1,
                                      padding=(2, 2), relief=tk.SUNKEN)
        self.copy_preview.grid(row=1, column=0, padx=4, sticky=tk.W+tk.E)
        tooltip.Tooltip(self.copy_preview, text='Min - Max interval')
        self.alert_on_interval = ttk.Label(self.editor_menu,
                                           image=self.neutral_icon)
        self.alert_on_interval.grid(row=1, column=1, padx=4)

        # options group frame
        self.options = ttk.LabelFrame(self, text="Options")
        self.options.columnconfigure(0, weight=1)
        self.options.columnconfigure(1, weight=1)
        self.options.columnconfigure(2, weight=2)
        self.options.grid(row=3, padx=4, pady=4, sticky=tk.W+tk.E)
        # measure offset - accepts a positive or negative number
        self.offset_checkbutton = ttk.Checkbutton(self.options, text='Offset',
                                                  variable=self.offset_option,
                                                  command=self.offset_cback)
        self.offset_checkbutton.grid(row=0, column=0, padx=4, pady=3, sticky=tk.W)
        # offset entry with validation
        self.change_sign = ttk.Button(self.options, text='+/-',
                                      command=self.change_value_sign,
                                      width=4)
        self.change_sign.grid(row=0, column=1, pady=3, sticky=tk.E)
        tooltip.Tooltip(self.change_sign, text='Change offset sign')
        self.offset_entry = ttk.Entry(self.options, width=10,
                                      validate='key',
                                      validatecommand=(self._validate_num,
                                                       '%S', '%P'))
        self.offset_entry.grid(row=0, column=2, padx=4, pady=3, sticky=tk.E)

        # new editor based on ttk.TreeView
        #self.new_editor = EditorFrame(self)
        #self.new_editor.grid(row=2, sticky='EW')
        #sono gli eventi nella vista principale a dover interagire con il controller

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
        self.offset_option.set(False)
        self.min_max_var.set(self.min_max_var.default)
        self.count_var.set('Count: 0')
        self.warning_label.configure(image=self.neutral_icon)
        self.warning_label.image = self.neutral_icon
        self.alert_on_interval.configure(image=self.neutral_icon)
        self.alert_on_interval.image = self.neutral_icon
        self.controller.set_values([])
        self.controller.set_offset(0.0)
        self.controller.set_precision(2)
        self.controller.set_tolerance({"min": 0.0, "max": 0.0})
        self.update()

    def export_as(self):
        ''' save as a file '''
        if self.controller.values:
            filename = filedialog.asksaveasfilename(initialdir="/%HOME",
                                                    title="Export to file",
                                                    defaultextension=".xlsx",
                                                    filetypes=(("XLSX files", "*.xlsx"),
                                                               ("SVG files", "*.svg"),
                                                               ("CSV files", "*.csv"),
                                                               ("all files", "*.*")))
            if filename.endswith('.svg'):
                self.controller.export_svg(filename)
            elif filename.endswith('.csv'):
                self.controller.export_to_csv(filename)
            else:
                self.controller.export_xlsx(filename)

    def view_stats(self):
        ''' View offline statistics '''
        pass
