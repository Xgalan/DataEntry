# -*- coding: utf-8 -*-
from __future__ import annotations

import string
import tkinter as tk
from contextlib import suppress
from tkinter import filedialog, messagebox
from typing import Protocol

import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.tooltip import ToolTip

from data_entry import icons


def validate_number(*args):
    list_of_num = list(string.digits)
    list_of_num.append(".")
    list_of_num.append("-")
    if args[0] in (list_of_num):
        return True
    else:
        return False


class Observer(Protocol):
    def update_from_subject(self, subject: Subject) -> None:
        pass


class Subject:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        with suppress(ValueError):
            self._observers.remove(observer)

    def notify(self, modifier: Observer | None = None) -> None:
        for observer in self._observers:
            if modifier != observer:
                observer.update_from_subject(self)


class Window(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        window_icon = tk.PhotoImage(data=icons.window_image)
        self.tk.call("wm", "iconphoto", self._w, window_icon)
        self.title("Data Entry")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main = MainFrame(self)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


class RibbonFrame(ttk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        # validation callbacks
        self._validate_num = self.register(validate_number)
        # icons
        self.delete_icon = tk.PhotoImage(data=icons.delete_image)
        self.save_icon = tk.PhotoImage(data=icons.save_image)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.__create_widgets()

    def __create_widgets(self):
        self.buttons = ttk.Frame(self)
        self.buttons.grid(row=0, column=0, sticky=tk.W + tk.E)
        # reset data entry button
        self.data_entry_clear = ttk.Button(
            self.buttons,
            command=self.master.clear_data_entry,
            text="Clear",
            width=8,
            compound=tk.TOP,
            image=self.delete_icon,
        )
        self.data_entry_clear.image = self.delete_icon
        self.data_entry_clear.grid(row=0, column=1, padx=1, pady=2)
        # save to file button
        self.save_btn = ttk.Button(
            self.buttons,
            text="Export as...",
            compound=tk.TOP,
            width=10,
            image=self.save_icon,
            command=self.master.export_as,
        )
        self.save_btn.image = self.save_icon
        self.save_btn.grid(row=0, column=2, padx=1, pady=2)
        # tooltips
        ToolTip(self.data_entry_clear, text="Clear content")
        ToolTip(self.save_btn, text="Export results as...")


class MainFrame(ttk.Frame, Subject):

    FRAME_WIDTH = 300

    def __init__(self, master=None) -> None:
        super().__init__(master)
        Subject.__init__(self)
        self._vars = {}
        self.green_icon = tk.PhotoImage(data=icons.green_led)
        self.neutral_icon = tk.PhotoImage(data=icons.neutral_led)
        self.yellow_icon = tk.PhotoImage(data=icons.yellow_led)
        self.alert_icon = tk.PhotoImage(data=icons.alert_triangle)
        self.sm_neutral_led = tk.PhotoImage(data=icons.sm_gray_led)
        self.sm_green_led = tk.PhotoImage(data=icons.sm_green_led)
        self.sm_yellow_led = tk.PhotoImage(data=icons.sm_yellow_led)
        self.copy_icon = tk.PhotoImage(data=icons.copy_image)

        # tk Vars initialization
        self.offset_option = tk.BooleanVar()
        self.min_max_var = tk.StringVar(value="- - - - - -")
        self.min_max_var.default = "- - - - - -"
        self.actual_min = tk.StringVar(value="- -")
        self.actual_max = tk.StringVar(value="- -")
        self.actual_min.default = "- -"
        self.actual_max.default = "- -"
        self.count_var = tk.StringVar(value="Count: 0")
        self.min_warning = tk.DoubleVar()
        self.max_warning = tk.DoubleVar()
        self.last_value = tk.StringVar(value="- - - - - -")
        self.units = tk.StringVar(value="mm")
        self.precision = tk.IntVar(value=2)
        # validation callbacks
        self._validate_num = self.register(validate_number)
        self.tolerance_is_set = False
        # configure style
        self.grid_columnconfigure(0, weight=1)
        self.grid()
        self.style = Style(theme="sandstone")
        self.__create_widgets()

    def flasher(self, widget, color) -> None:
        """Change the background color of a widget for 100ms."""

        def change_color(widget, color):
            widget.config(background=color)

        orig_color = widget.cget("background")
        self.count_label.after(10, change_color, widget, color)
        self.count_label.after(100, change_color, widget, orig_color)

    def alert(self, **kwargs):
        """show an alert message if the editor has no content."""
        with suppress(AttributeError):
            tk.messagebox.showwarning("Missing values", kwargs["msg"])

    def update_from_model(self, model) -> None:
        """observer pattern"""
        # TODO: move this methods to the right place

        def set_green_icon(obj_ref):
            obj_ref.configure(image=self.green_icon)
            obj_ref.image = self.green_icon

        def set_yellow_icon(obj_ref):
            obj_ref.configure(image=self.yellow_icon)
            obj_ref.image = self.yellow_icon

        def set_sm_green_led(obj_ref):
            obj_ref.configure(image=self.sm_green_led)
            obj_ref.image = self.sm_green_led

        def set_sm_yellow_led(obj_ref):
            obj_ref.configure(image=self.sm_yellow_led)
            obj_ref.image = self.sm_yellow_led

        min_v = model.tolerance["min"]
        max_v = model.tolerance["max"]
        model_min = model.min()
        model_max = model.max()
        self.count_var.set("Count: " + str(len(model.values)))
        self.min_max_var.set(model.min_max())
        self.actual_min.set(model_min)
        self.actual_max.set(model_max)
        try:
            # TODO case if first value is zero i.e., "0.00"
            last_val = round(model.values[-1], model.precision)
            self.last_value.set(str(last_val) + " " + model.units.units)
            if self.tolerance_is_set:
                if last_val >= min_v and last_val <= max_v:
                    set_green_icon(self.warning_label)
                else:
                    set_yellow_icon(self.warning_label)
                if model_min < min_v or model_max > max_v:
                    set_yellow_icon(self.alert_on_interval)
                else:
                    set_green_icon(self.alert_on_interval)
                if model_min < min_v:
                    set_sm_yellow_led(self.min_led)
                else:
                    set_sm_green_led(self.min_led)
                if model_max > max_v:
                    set_sm_yellow_led(self.max_led)
                else:
                    set_sm_green_led(self.max_led)
        except IndexError:
            self.last_value.set("No valid value")

    def offset_cback(self) -> float:
        with suppress(ValueError):
            # check if the user has entered an offset value
            if self.offset_option.get() is True:
                self._vars["offset"] = float(self.offset_entry.get())
            else:
                self._vars["offset"] = 0.0
            self.notify()
            return self.offset_option.get()

    def __set_values(self, *args) -> None:
        text = self.get_editor_content()
        if text is not None:
            self._vars["text"] = text.splitlines()
            self.flasher(self.count_label, "snow2")
            self.notify()

    def __set_units(self, event) -> None:
        self._vars["units"] = self.units_cb.get()
        self.notify()

    def __set_precision(self, event) -> None:
        self._vars["precision"] = int(self.precision.get())
        self.notify()

    def __set_tolerance(self) -> None:
        self.tolerance_is_set = True
        self._vars["tolerance"] = {
            "min": float(self.min_dim.get()),
            "max": float(self.max_dim.get()),
        }
        self.notify()

    def __create_widgets(self) -> None:
        # ribbon menu
        self.ribbon = RibbonFrame(self)
        self.ribbon["padding"] = (1, 1)
        self.ribbon["borderwidth"] = 1
        self.ribbon.grid(row=1, column=0, sticky=tk.N + tk.W)
        # editor
        self.editor = ttk.Frame(self, borderwidth=1, width=self.FRAME_WIDTH)
        self.editor.grid(row=2, column=0, pady=2, sticky=tk.W + tk.E)
        self.data_entry = ScrolledText(self.editor, padding=2, width=32, autohide=True)
        self.data_entry.grid(row=0, column=0, padx=1, ipadx=2, sticky=tk.W + tk.E)
        # update event on data entry text widget
        self.data_entry.text.bind("<Return>", self.__set_values)
        # model elements count
        self.count_label = ttk.Label(
            self.editor,
            textvariable=self.count_var,
            font=("Helvetica", 12, "bold"),
            padding=(1, 1),
        )
        self.count_label.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=1,
            pady=0,
            ipadx=2,
            ipady=2,
            sticky=tk.W + tk.E,
        )
        # passed/failed frame
        self.editor_menu = ttk.Frame(self)
        self.editor_menu.columnconfigure(0, weight=2)
        self.editor_menu.columnconfigure(1, weight=1)
        self.editor_menu.grid(row=3, column=0, pady=2, sticky=tk.W + tk.E)

        # good/warning icon
        self.warning_label = ttk.Label(self.editor_menu, image=self.neutral_icon)
        self.warning_label.grid(row=1, column=1, padx=4)
        self.last_value_with_offset = ttk.Label(
            self.editor_menu,
            width=16,
            borderwidth=1,
            font=("Helvetica", 12, "bold"),
            padding=(2, 2),
            textvariable=self.last_value,
        )
        self.last_value_with_offset.grid(row=1, column=0, padx=4, sticky=tk.W + tk.E)
        ToolTip(self.last_value_with_offset, text="Last value")
        # min - max values
        self.copy_preview = ttk.Label(
            self.editor_menu,
            textvariable=self.min_max_var,
            font=("Helvetica", 12, "bold"),
            borderwidth=1,
            padding=(2, 2),
        )
        self.copy_preview.grid(row=2, column=0, padx=4, sticky=tk.W + tk.E)
        ToolTip(self.copy_preview, text="Min - Max interval")
        self.alert_on_interval = ttk.Label(self.editor_menu, image=self.neutral_icon)
        self.alert_on_interval.grid(row=2, column=1, padx=4)
        # dimensions group
        self.dimensions = ttk.LabelFrame(self, text="Dimensions")
        self.dimensions.columnconfigure(0, weight=1)
        self.dimensions.columnconfigure(1, weight=2)
        self.dimensions.columnconfigure(2, weight=2)
        self.dimensions.grid(row=4, padx=4, pady=4, sticky=tk.W + tk.E)
        # min/max allowed dimensions
        self.min_dim_label = ttk.Label(self.dimensions, anchor=tk.E, text="Min.")
        self.max_dim_label = ttk.Label(self.dimensions, anchor=tk.E, text="Max.")
        self.min_led = ttk.Label(self.dimensions, image=self.sm_neutral_led)
        self.max_led = ttk.Label(self.dimensions, image=self.sm_neutral_led)
        self.min_dim_label.grid(row=0, column=1, padx=4, pady=3, sticky=tk.E)
        self.max_dim_label.grid(row=0, column=3, padx=4, pady=3, sticky=tk.E)
        self.min_led.grid(row=0, column=2, padx=2, sticky=tk.E)
        self.max_led.grid(row=0, column=4, padx=2, sticky=tk.E)
        # nominal dimensions
        self.nominal_label = ttk.Label(self.dimensions, anchor=tk.E, text="Nominal:")
        self.min_dim = ttk.Entry(
            self.dimensions,
            width=10,
            validate="key",
            validatecommand=(self._validate_num, "%S", "%P"),
            textvariable=self.min_warning,
            justify=tk.RIGHT,
        )
        self.max_dim = ttk.Entry(
            self.dimensions,
            width=10,
            validate="key",
            validatecommand=(self._validate_num, "%S", "%P"),
            textvariable=self.max_warning,
            justify=tk.RIGHT,
        )
        self.nominal_label.grid(row=1, column=0, pady=3, sticky=tk.W + tk.E)
        self.min_dim.grid(row=1, column=1, columnspan=2, padx=2, pady=3, sticky=tk.E)
        self.max_dim.grid(row=1, column=3, columnspan=2, padx=2, pady=3, sticky=tk.E)
        # actual dimensions
        self.actual_label = ttk.Label(self.dimensions, anchor=tk.E, text="Actual:")
        self.actual_label.grid(row=2, column=0, pady=3, sticky=tk.W + tk.E)
        self.min_entry = ttk.Entry(
            self.dimensions,
            width=10,
            textvariable=self.actual_min,
            justify=tk.RIGHT,
            state="readonly",
        )
        self.max_entry = ttk.Entry(
            self.dimensions,
            width=10,
            textvariable=self.actual_max,
            justify=tk.RIGHT,
            state="readonly",
        )
        self.min_entry.grid(row=2, column=1, columnspan=2, padx=2, pady=3, sticky=tk.E)
        self.max_entry.grid(row=2, column=3, columnspan=2, padx=2, pady=3, sticky=tk.E)
        # tooltips
        ToolTip(self.min_dim, text="Enter lower dimension")
        ToolTip(self.max_dim, text="Enter upper dimension")

        # Set / Reset buttons
        self.set_reset = ttk.Frame(self.dimensions, width=10)
        self.set_reset.grid(row=3, column=0, columnspan=5, padx=2, sticky=tk.E)
        # copy to clipboard
        self.copy_to_clip = ttk.Button(
            self.set_reset,
            command=self.cp_to_clipboard,
            text="Copy",
            compound=tk.LEFT,
            width=6,
            image=self.copy_icon,
        )
        self.copy_to_clip.image = self.copy_icon
        self.copy_to_clip.grid(row=0, column=0, padx=2, pady=3, sticky=tk.E)

        self.reset = ttk.Button(
            self.set_reset, command=self.reset_tolerance, text="Reset", width=4
        )
        self.reset.grid(row=0, column=1, padx=2, pady=3, sticky=tk.E)
        self.set = ttk.Button(
            self.set_reset, command=self.__set_tolerance, text="Set", width=4
        )
        self.set.grid(row=0, column=2, padx=2, pady=3, sticky=tk.E)
        ToolTip(self.copy_to_clip, text="Copy to clipboard")

        # measure options group frame
        self.options = ttk.LabelFrame(self, text="Options")
        self.options.columnconfigure(0, weight=1)
        self.options.columnconfigure(1, weight=1)
        self.options.columnconfigure(2, weight=2)
        self.options.grid(row=5, padx=4, pady=4, sticky=tk.W + tk.E)

        # measure offset - accepts a positive or negative number
        self.offset_checkbutton = ttk.Checkbutton(
            self.options,
            text="Offset",
            variable=self.offset_option,
            width=14,
            command=self.offset_cback,
        )
        self.offset_checkbutton.grid(row=0, column=0, padx=4, pady=3, sticky=tk.W)
        # offset entry with validation
        self.change_sign = ttk.Button(
            self.options,
            text="\261",
            style="Bold.TButton",
            command=self.change_value_sign,
            width=4,
        )
        self.offset_entry = ttk.Entry(
            self.options,
            width=8,
            validate="key",
            validatecommand=(self._validate_num, "%S", "%P"),
        )
        ToolTip(self.change_sign, text="Change offset sign")
        self.offset_entry.grid(row=0, column=1, padx=0, pady=3, sticky=tk.E)
        self.change_sign.grid(row=0, column=2, padx=4, pady=3, sticky=tk.E)
        # units of measurements settings
        self.um_options = ttk.Frame(self.options)
        self.um_options.grid(row=1, columnspan=3, padx=4, pady=3, sticky=tk.W + tk.E)
        self.um_options_label = ttk.Label(self.um_options, text="Units:", width=14)
        self.um_options_label.grid(row=0, column=0)
        self.units_cb = ttk.Combobox(
            self.um_options,
            textvariable=self.units,
            state="readonly",
            width=10,
            values=["mm", "um", "cm", "m", "g"],
        )
        self.units_cb.bind("<<ComboboxSelected>>", self.__set_units)
        self.units_cb.grid(row=0, column=1, padx=1, pady=2, sticky=tk.N + tk.E)
        self.precision_e = ttk.Entry(
            self.um_options,
            textvariable=self.precision,
            validate="key",
            validatecommand=(self._validate_num, "%S", "%P"),
            width=4,
        )
        self.precision_e.bind("<Return>", self.__set_precision)
        self.precision_e.grid(row=0, column=2, padx=1, pady=2, sticky=tk.E)
        ToolTip(self.units_cb, text="Choose unit of measurement")
        ToolTip(self.precision_e, text="Enter decimals")

    def get_editor_content(self):
        """check if the editor is empty or return the content."""
        text = self.data_entry.text.get("1.0", "end-1c")
        if text == "":
            text = None
            self.alert(msg="Please insert some values in the editor.")
            pass
        else:
            return text

    def change_value_sign(self) -> None:
        offset_val = self.offset_entry.get()
        if offset_val.find("-", 0, 1) != -1:
            self.offset_entry.delete(0, 1)
            self.offset_option.set(False)
        else:
            self.offset_entry.insert(0, "-")
            self.offset_option.set(False)

    def cp_to_clipboard(self) -> None:
        """
        copy to clipboard the converted values from the text editor.
        """
        self.clipboard_clear()
        text = self.get_editor_content()
        if text is not None:
            self.clipboard_append(self.min_max_var.get())
        self.update()

    def reset_warning_icons(self) -> None:
        # "reset" icons
        self.warning_label.configure(image=self.neutral_icon)
        self.warning_label.image = self.neutral_icon
        self.alert_on_interval.configure(image=self.neutral_icon)
        self.alert_on_interval.image = self.neutral_icon
        self.min_led.configure(image=self.sm_neutral_led)
        self.max_led.configure(image=self.sm_neutral_led)
        self.min_led.image = self.sm_neutral_led
        self.max_led.image = self.sm_neutral_led

    def clear_data_entry(self) -> None:
        """delete the content of the editor and delete the values of the options."""
        # editor and associated variables
        self.data_entry.delete("1.0", "end-1c")
        self.data_entry.edit_modified(False)
        self._vars["text"] = []
        # offset option reset
        self.offset_entry.delete(0, tk.END)
        self._vars["offset"] = 0.0
        self.offset_option.set(False)
        # reset tkVars
        self.count_var.set("Count: 0")
        self.min_max_var.set(self.min_max_var.default)
        self.actual_min.set(self.actual_min.default)
        self.actual_max.set(self.actual_max.default)
        # reset other vars
        self._vars["precision"] = 2
        self.reset_warning_icons()
        self.notify()

    def reset_tolerance(self) -> None:
        self.min_warning.set(0.0)
        self.max_warning.set(0.0)
        self._vars["tolerance"] = {"min": 0.0, "max": 0.0}
        self.reset_warning_icons()
        self.tolerance_is_set = False
        self.notify()

    def export_as(self) -> None:
        """save as a file"""
        if self.count_var.get() != "Count: 0":
            filename = filedialog.asksaveasfilename(
                initialdir="/%HOME",
                title="Export to file",
                defaultextension=".csv",
                filetypes=(
                    ("CSV files", "*.csv"),
                    ("JSON files", "*.json"),
                    ("all files", "*.*"),
                ),
            )
            self._vars["filename"] = filename
            self.notify()
        else:
            self.alert(msg="Please insert some values in the editor.")
