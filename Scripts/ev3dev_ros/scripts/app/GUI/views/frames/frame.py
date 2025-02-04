#!/usr/bin/env python3

from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton, QGridLayout, QWidget
import app.gui.styles.styles as styles


class BaseFrame(QFrame):

    def __init__(self, parent: QWidget, mqtt_client, delegate, padding=20):
        super().__init__(parent)
        self.delegate = delegate
        self.mqtt_client = mqtt_client

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(padding, padding, padding, padding)

        # Aplicar estilo al Frame
        self.style_frame = styles.StyleFrame()
        self.style_frame.apply_style(self)

    def create_label(self, text, row, col):
        label = QLabel(text)
        self.layout.addWidget(label, row, col)
        return label

    def create_entry(self, row, col, text="", width=8):
        entry = QLineEdit()
        entry.setMaxLength(width)
        entry.setText(text)
        self.layout.addWidget(entry, row, col)
        return entry

    def create_button(self, text, row, col, command):
        button = QPushButton(text)
        button.clicked.connect(command)
        self.layout.addWidget(button, row, col)
        return button

    def get_widgets_by_type(self, widget_type):
        """Devuelve una lista de widgets de un tipo específico dentro del layout."""
        return [self.layout.itemAt(i).widget() for i in range(self.layout.count())
                if isinstance(self.layout.itemAt(i).widget(), widget_type)]

    def get_buttons(self):
        return self.get_widgets_by_type(QPushButton)

    def get_entries(self):
        return self.get_widgets_by_type(QLineEdit)

    def get_labels(self):
        return self.get_widgets_by_type(QLabel)

    def style_buttons(self):
        style_button = styles.StyleButton()
        for button in self.get_buttons():
            style_button.apply_style(button)

    def style_labels(self):
        style_label = styles.StyleLabel()
        for label in self.get_labels():
            style_label.apply_style(label)

    def style_entries(self):
        style_entry = styles.StyleEntry()
        for entry in self.get_entries():
            style_entry.apply_style(entry)
