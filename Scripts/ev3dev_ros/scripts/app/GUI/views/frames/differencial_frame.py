#!/usr/bin/env python3

import tkinter
import app.mqtt.messages as messages
import app.gui.views.frames.frame as frame
import app.gui.controls.buttons as buttons_controls

class DifferencialFrame(frame.BaseFrame):

    def __init__(self, master, mqtt_client, delegate, padding=20):
        super().__init__(master, mqtt_client, delegate, padding)

        self.buttons_controls = buttons_controls.DifferentialControlButtons(self.master, self.mqtt_client)

        self.create_widgets()

        self.style_buttons()
        self.style_labels()
        self.style_entries()

        self.master.bind('<a>', lambda event: messages.send_message_special(self.mqtt_client, "Angle", "angle key"))

        self.master.bind('<Up>', lambda event: messages.send_message_movtank(self.mqtt_client, int(self.left_speed_entry.get()), int(self.right_speed_entry.get()), "Forward key"))

        self.master.bind('<Left>', lambda event: messages.send_message_movtank(self.mqtt_client, (-1/2)*int(self.left_speed_entry.get()), (1/2)*int(self.right_speed_entry.get()), "Left key"))

        self.master.bind('<space>', lambda event: messages.send_message_special(self.mqtt_client, "Stop", "Stop key"))

        self.master.bind('<Right>', lambda event: messages.send_message_movtank(self.mqtt_client, (1/2)*int(self.left_speed_entry.get()), (-1/2)*int(self.right_speed_entry.get()), "Right key"))

        self.master.bind('<Down>', lambda event: messages.send_message_movtank(self.mqtt_client, (-1)*int(self.left_speed_entry.get()), (-1)*int(self.right_speed_entry.get()), "Back key"))

        self.master.bind('<u>', lambda event: messages.send_message_special(self.mqtt_client, "arm_up", "Up key"))

        self.master.bind('<j>', lambda event: messages.send_message_special(self.mqtt_client, "arm_down", "Down key"))

        self.master.bind('<q>', lambda event: messages.send_message_special(self.mqtt_client, "Quit", "Quit key"))

        self.master.bind('<e>', lambda event: exit())
  
    def create_widgets(self):
        self.grid()
        self.pack(padx=2, pady=2, fill='both', expand=True)

        """Creación de cuadro de texto para obtener valor de velocidad
        del motor izquierdo y etiqueta descritiva para el usuario"""
        self.left_speed_label = self.create_label("Left", 0, 0)
        self.left_speed_entry = self.create_entry(1, 0, text="100", justify=tkinter.LEFT)
        self.buttons_controls.set_left_speed_entry(self.left_speed_entry)

        """Creación de cuadro de texto para obtener valor de velocidad
        del motor derecho y etiqueta descritiva para el usuario"""
        self.right_speed_label = self.create_label("Right", 0, 2)
        self.right_speed_entry = self.create_entry(1, 2, text="100", justify=tkinter.RIGHT)
        self.buttons_controls.set_right_speed_entry(self.right_speed_entry)

        """Creación de label para presnetar el valor de ángulo recibido y
        declaración en el objeto my_delagate del label que recibe dicho mensaje"""
        self.angle_label = self.create_label("Angle", 0, 3)
        self.angle_value_label = self.create_label("0", 1, 3)
        self.buttons_controls.set_angle_value_label(self.angle_value_label)
        self.delegate.setlabel(self.angle_value_label)

        """Creación de los botones"""
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





