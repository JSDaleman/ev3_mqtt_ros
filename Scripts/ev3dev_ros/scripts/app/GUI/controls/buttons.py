#!/usr/bin/env python3

import app.mqtt.messages as messages

class ControlButtons():
    def __init__(self, master, mqtt_client):
        self.master = master
        self.mqtt_client = mqtt_client

class DifferentialControlButtons(ControlButtons):

    def __init__(self, master, mqtt_client):
        super().__init__(master, mqtt_client)
        self.right_speed_entry = None
        self.left_speed_entry = None
        self.angle_value_label = None

    def set_right_speed_entry(self, right_speed_entry):
        self.right_speed_entry = right_speed_entry
    
    def set_left_speed_entry(self, left_speed_entry):
        self.left_speed_entry = left_speed_entry
    
    def set_angle_value_label(self, angle_value_label):
        self.angle_value_label = angle_value_label

    def send_angle_message(self):
        messages.send_message_special(self.mqtt_client, "Angle", "angle button")

    def send_forward_message(self):
        try:
            value_right = int(self.right_speed_entry.get())
            value_left = int(self.left_speed_entry.get())
            speed = max(value_right, value_left)
            messages.send_message_movtank(self.mqtt_client, speed, speed, "Forward button")

        except ValueError:
            print("Please enter a valid number")

    def send_left_message(self):
        try:
            value_right = int(self.right_speed_entry.get())
            value_left = int(self.left_speed_entry.get())

            if value_left == value_right:
                messages.send_message_movtank(self.mqtt_client, -1*value_left, 1*value_right, "Left button")
            else:
                speed = min(value_right, value_left)
                messages.send_message_movtank(self.mqtt_client, -1*speed, 1*speed, "Left button")

        except ValueError:
            print("Please enter a valid number")

    def send_stop_message(self):
        messages.send_message_special(self.mqtt_client, "Stop", "Stop button")

    def send_right_message(self):
        try:
            value_right = int(self.right_speed_entry.get())
            value_left = int(self.left_speed_entry.get())

            if value_left == value_right:
                messages.send_message_movtank(self.mqtt_client, 1*value_left, -1*value_right, "Right button")
            else:
                speed = min(value_right, value_left)
                messages.send_message_movtank(self.mqtt_client, 1*speed, -1*speed, "Right button")

        except ValueError:
            print("Please enter a valid number")

    def send_back_message(self):
        try:
            value_right = int(self.right_speed_entry.get())
            value_left = int(self.left_speed_entry.get())
            speed = min(value_right, value_left)
            messages.send_message_movtank(self.mqtt_client, -1*speed, -1*speed, "Back button")

        except ValueError:
            print("Please enter a valid number")

    def send_up_message(self):
        messages.send_message_special(self.mqtt_client, "arm_up", "Up button")

    def send_down_message(self):
        messages.send_message_special(self.mqtt_client, "arm_down", "Down button")

    def send_quit_message(self):
        messages.send_message_special(self.mqtt_client, "Quit", "Quit button")

    def send_exit(self):
        exit()