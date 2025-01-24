#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import app.gui.styles.styles as styles

class BaseFrame(ttk.Frame):

    def __init__(self, master, mqtt_client, delegate, padding=20):
        super().__init__(master, padding=padding)
        self.delegate = delegate
        self.mqtt_client = mqtt_client

        StyleFrame = styles.StyleFrame(self.master) 
        StyleFrame.apply_style(self)

    def create_widgets(self):
        self.grid()

    def create_label(self, text, row, col):
        label = ttk.Label(self, text=text)
        label.grid(row=row, column=col)
        return label

    def create_entry(self, row, col, index=0, text="", width=8, justify=tk.CENTER):
        entry = ttk.Entry(self, width=width, justify=justify)
        entry.insert(index, text)
        entry.grid(row=row, column=col)
        return entry

    def create_button(self, text, row, col, command):
        button = ttk.Button(self, text=text, command=command)
        button.grid(row=row, column=col)
        return button

    def get_buttons(self):
        buttons = []
        for widget in self.winfo_children():
            if isinstance(widget, (tk.Button, ttk.Button)):  # Verificar si el widget es un botón
                buttons.append(widget)
        return buttons
    
    def get_entries(self):
        entries = []
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Entry):  # Verificar si el widget es un Entry
                entries.append(widget)
        return entries

    def get_labels(self):
        labels = []
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Label):  # Verificar si el widget es un Label
                labels.append(widget)
        return labels

    def style_buttons(self):
        StyleButton = styles.StyleButton(self)
        for button in self.get_buttons():
            StyleButton.apply_style(button)

    def style_labels(self):
        StyleLabel = styles.StyleLabel(self)
        for label in self.get_labels():
            StyleLabel.apply_style(label)

    def style_entries(self):
        StyleEntry = styles.StyleEntry(self)
        for entry in self.get_entries():
            StyleEntry.apply_style(entry)