#!/usr/bin/env python3

from PyQt5.QtWidgets import QLineEdit, QLabel
import app.mqtt.messages as messages

class ControlButtons():
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

class DifferentialControlButtons(ControlButtons):

    def __init__(self, mqtt_client):
        super().__init__(mqtt_client)
        self.right_speed_entry: QLineEdit = None
        self.left_speed_entry: QLineEdit = None
        self.angle_value_label: QLabel = None


    def set_right_speed_entry(self, right_speed_entry: QLineEdit):
        self.right_speed_entry = right_speed_entry
    
    def set_left_speed_entry(self, left_speed_entry: QLineEdit):
        self.left_speed_entry = left_speed_entry

    def set_angle_value_label(self, label: QLabel):
        self.angle_value_label = label
    
    def send_angle_message(self):
        messages.send_message_special(self.mqtt_client, "Angle", "angle button")

    def send_forward_message(self):
        self._send_movement_message(1, 1, "Forward button")

    def send_left_message(self):
        self._send_movement_message(-1, 1, "Left button")

    def send_right_message(self):
        self._send_movement_message(1, -1, "Right button")

    def send_back_message(self):
        self._send_movement_message(-1, -1, "Back button")

    def send_stop_message(self):
        messages.send_message_special(self.mqtt_client, "Stop", "Stop button")

    def send_up_message(self):
        messages.send_message_special(self.mqtt_client, "arm_up", "Up button")

    def send_down_message(self):
        messages.send_message_special(self.mqtt_client, "arm_down", "Down button")

    def send_quit_message(self):
        messages.send_message_special(self.mqtt_client, "Quit", "Quit button")

    def send_exit(self):
        messages.send_message_special(self.mqtt_client, "shutdown", "Exit key")
        self.mqtt_client.close()
        exit()

    def _send_movement_message(self, factor_left, factor_right, action_name):
        """ Función para enviar mensajes de movimiento con los valores de los inputs. """
        try:
            value_right = int(self.right_speed_entry.text())
            value_left = int(self.left_speed_entry.text())
            speed = min(value_right, value_left)
            messages.send_message_movtank(self.mqtt_client, factor_left * speed, factor_right * speed, action_name)
        except ValueError:
            print("Por favor ingrese un número válido.")

