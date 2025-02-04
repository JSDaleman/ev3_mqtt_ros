#!/usr/bin/env python3

from PyQt5.QtWidgets import QLineEdit, QWidget, QLabel
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
import app.mqtt.messages as messages
import sys

class ControlKeys(QWidget):
    def __init__(self, mqtt_client):
        super().__init__()
        self.mqtt_client = mqtt_client

class DifferentialControlKeys(ControlKeys):
    def __init__(self, mqtt_client):
        super().__init__(mqtt_client)
        self.right_speed_entry: QLineEdit = None
        self.left_speed_entry: QLineEdit = None
        self.angle_value_label: QLabel = None
       #self.setFocusPolicy(Qt.StrongFocus)

        self.key_map = {
            Qt.Key_Up: self.control_key_up,
            Qt.Key_Left: self.control_key_left,
            Qt.Key_Right: self.control_key_right,
            Qt.Key_Down: self.control_key_down,
            Qt.Key_A: lambda: messages.send_message_special(self.mqtt_client, "Angle", "angle key"),
            Qt.Key_Space: lambda: messages.send_message_special(self.mqtt_client, "Stop", "Stop key"),
            Qt.Key_U: lambda: messages.send_message_special(self.mqtt_client, "arm_up", "Up key"),
            Qt.Key_J: lambda: messages.send_message_special(self.mqtt_client, "arm_down", "Down key"),
            Qt.Key_Q: lambda: messages.send_message_special(self.mqtt_client, "Quit", "Quit key"),
            Qt.Key_E: self.control_key_e
        }

    def set_right_speed_entry(self, right_speed_entry: QLineEdit):
        self.right_speed_entry = right_speed_entry

    def set_left_speed_entry(self, left_speed_entry: QLineEdit):
        self.left_speed_entry = left_speed_entry

    def set_angle_value_label(self, label: QLabel):
        self.angle_value_label = label

    def control_key_up(self):
        self._send_movement_message(1, 1, "Forward key")

    def control_key_left(self):
        self._send_movement_message(-1, 1, "Left key")

    def control_key_right(self):
        self._send_movement_message(1, -1, "Right key")

    def control_key_down(self):
        self._send_movement_message(-1, -1, "Back key")

    def control_key_e(self):
        messages.send_message_special(self.mqtt_client, "shutdown", "Exit key")
        sys.exit()

    def _send_movement_message(self, factor_left, factor_right, action_name):
        """ Envía mensajes de movimiento con los valores de entrada. """

        try:
            value_right = int(self.right_speed_entry.text())
            value_left = int(self.left_speed_entry.text())
            speed = min(value_right, value_left)
            messages.send_message_movtank(self.mqtt_client, factor_left * speed, factor_right * speed, action_name)
        except ValueError:
            print("Por favor ingrese un número válido.")

    def keyPressEvent(self, event: QKeyEvent):
        """ Captura eventos de teclado y ejecuta la acción correspondiente. """
        if event.key() in self.key_map:
            self.key_map[event.key()]()
            event.accept()

