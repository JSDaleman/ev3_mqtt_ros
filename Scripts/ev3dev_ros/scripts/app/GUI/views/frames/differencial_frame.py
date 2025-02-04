#!/usr/bin/env python3
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QKeyEvent
import app.gui.views.frames.frame as frame
import app.gui.controls.buttons as buttons_controls
import app.gui.controls.keys as keys_controls


class DifferencialFrame(frame.BaseFrame):

    def __init__(self, parent, mqtt_client, delegate, padding=20):
        super().__init__(parent, mqtt_client, delegate, padding)

        self.buttons_controls = buttons_controls.DifferentialControlButtons(self.mqtt_client)
        self.keys_controls = keys_controls.DifferentialControlKeys(self.mqtt_client)
        self.setFocusPolicy(Qt.StrongFocus)

        self.create_widgets()

        self.style_buttons()
        self.style_labels()
        self.style_entries()

        #self.keys_controls.set_keys_control()

    def create_widgets(self):
        """ Creación de cuadro de texto para obtener valor de velocidad 
            del motor izquierdo y etiqueta descriptiva para el usuario """
        self.left_speed_label = self.create_label("Left", 0, 0)
        self.left_speed_entry = self.create_entry(1, 0, text="100")
        self.buttons_controls.set_left_speed_entry(self.left_speed_entry)
        self.keys_controls.set_left_speed_entry(self.left_speed_entry)

        """ Creación de cuadro de texto para obtener valor de velocidad 
            del motor derecho y etiqueta descriptiva para el usuario """
        self.right_speed_label = self.create_label("Right", 0, 2)
        self.right_speed_entry = self.create_entry(1, 2, text="100")
        self.buttons_controls.set_right_speed_entry(self.right_speed_entry)
        self.keys_controls.set_right_speed_entry(self.right_speed_entry)

        """ Creación de label para presentar el valor de ángulo recibido 
            y declaración en el objeto delegate del label que recibe dicho mensaje """
        self.angle_label = self.create_label("Angle", 0, 3)
        self.angle_value_label = self.create_label("0", 1, 3)
        self.buttons_controls.set_angle_value_label(self.angle_value_label)
        self.keys_controls.set_angle_value_label(self.angle_value_label)
        self.delegate.setlabel(self.angle_value_label)

        """ Creación de los botones """
        self.angle_button = self.create_button("Update angle", 2, 3, self.buttons_controls.send_angle_message)
        self.forward_button = self.create_button("Forward", 2, 1, self.buttons_controls.send_forward_message)
        self.left_button = self.create_button("Left", 3, 0, self.buttons_controls.send_left_message)
        self.stop_button = self.create_button("Stop", 3, 1, self.buttons_controls.send_stop_message)
        self.right_button = self.create_button("Right", 3, 2, self.buttons_controls.send_right_message)
        self.back_button = self.create_button("Back", 4, 1, self.buttons_controls.send_back_message)
        self.up_button = self.create_button("Up", 5, 0, self.buttons_controls.send_up_message)
        self.down_button = self.create_button("Down", 6, 0, self.buttons_controls.send_down_message)
        self.q_button = self.create_button("Quit", 5, 2, self.buttons_controls.send_quit_message)
        self.e_button = self.create_button("Exit", 6, 2, self.buttons_controls.send_exit)

    def keyPressEvent(self, event):
        QCoreApplication.postEvent(self.keys_controls, QKeyEvent(event))
