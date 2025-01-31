#!/usr/bin/env python3

import app.mqtt.messages as messages

class ControlKeys():
      
      def __init__(self, master, mqtt_client):
        self.master = master
        self.mqtt_client = mqtt_client

class DifferentialControlKeys(ControlKeys):
      
    def __init__(self, master, mqtt_client):
        super().__init__(master, mqtt_client)

        self.right_speed_entry = None
        self.left_speed_entry = None
        self.angle_value_label = None

        self.entries = [self.right_speed_entry, self.left_speed_entry]

    def set_right_speed_entry(self, right_speed_entry):
        self.right_speed_entry = right_speed_entry
    
    def set_left_speed_entry(self, left_speed_entry):
        self.left_speed_entry = left_speed_entry
    
    def set_angle_value_label(self, angle_value_label):
        self.angle_value_label = angle_value_label

    def remove_focus(self, event):
        # Si el clic no es sobre el Entry, quita el enfoque
        if event.widget not in [self.right_speed_entry, self.left_speed_entry]:
            self.master.focus()

    def block_keys(self):

        focused_widget = self.master.focus_get()

        if focused_widget in [self.right_speed_entry, self.left_speed_entry]:
            # Comportamiento cuando el Entry tiene el enfoque
            return True
        
        return False

    def control_key_up(self, event):
        try:
            value_right = int(self.right_speed_entry.get())
            value_left = int(self.left_speed_entry.get())
            speed = max(value_right, value_left)
            messages.send_message_movtank(self.mqtt_client, speed, speed, "Forward key")

        except ValueError:
            print("Please enter a valid number")

    def control_key_left(self, event):

        if self.block_keys():
            return
        
        # Comportamiento cuando el Entry NO tiene el enfoque
        try:
            value_right = int(self.right_speed_entry.get())
            value_left = int(self.left_speed_entry.get())

            if value_left == value_right:
                messages.send_message_movtank(self.mqtt_client, -1*value_left, 1*value_right, "Left key")
            else:
                speed = min(value_right, value_left)
                messages.send_message_movtank(self.mqtt_client, -1*speed, 1*speed, "Left key")

        except ValueError:
            print("Please enter a valid number")

        return "break"  # Bloquea el comportamiento predeterminado de la tecla


    def control_key_right(self, event):

        if self.block_keys():
            return
        
        # Comportamiento cuando el Entry NO tiene el enfoque
        try:
            value_right = int(self.right_speed_entry.get())
            value_left = int(self.left_speed_entry.get())

            if value_left == value_right:
                messages.send_message_movtank(self.mqtt_client, 1*value_left, -1*value_right, "Right key")
            else:
                speed = min(value_right, value_left)
                messages.send_message_movtank(self.mqtt_client, 1*speed, -1*speed, "Right key")

        except ValueError:
            print("Please enter a valid number")

        return "break"  # Bloquea el comportamiento predeterminado de la tecla
    
    def control_key_down(self, event):
        try:
            value_right = int(self.right_speed_entry.get())
            value_left = int(self.left_speed_entry.get())
            speed = min(value_right, value_left)
            messages.send_message_movtank(self.mqtt_client, -1*speed, -1*speed, "Back key")

        except ValueError:
            print("Please enter a valid number")

    def set_keys_control(self):

        self.master.bind("<Button-1>", lambda event: self.remove_focus(event))

        self.master.bind('<Up>', lambda event: self.control_key_up(event))
        self.master.bind('<Left>', lambda event: self.control_key_left(event))
        self.master.bind('<Right>', lambda event: self.control_key_right(event))
        self.master.bind('<Down>', lambda event: self.control_key_down(event))

        self.master.bind('<a>', lambda event: messages.send_message_special(self.mqtt_client, "Angle", "angle key"))
        self.master.bind('<space>', lambda event: messages.send_message_special(self.mqtt_client, "Stop", "Stop key"))
        self.master.bind('<u>', lambda event: messages.send_message_special(self.mqtt_client, "arm_up", "Up key"))
        self.master.bind('<j>', lambda event: messages.send_message_special(self.mqtt_client, "arm_down", "Down key"))
        self.master.bind('<q>', lambda event: messages.send_message_special(self.mqtt_client, "Quit", "Quit key"))
        self.master.bind('<e>', lambda event: exit())
        

        

    
