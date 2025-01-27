#!/usr/bin/env python3

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

    def set_right_speed_entry(self, right_speed_entry):
        self.right_speed_entry = right_speed_entry
    
    def set_left_speed_entry(self, left_speed_entry):
        self.left_speed_entry = left_speed_entry
    
    def set_angle_value_label(self, angle_value_label):
        self.angle_value_label = angle_value_label
    
    def manejar_tecla_right(root, event, entry):
        if root.focus_get() == entry:
            # Comportamiento cuando el Entry tiene el enfoque
            print("Cursor moviéndose a la derecha dentro del Entry")
            return
        else:
            # Comportamiento cuando el Entry NO tiene el enfoque
            print("Hola mundo (tecla Right fuera del Entry)")
            return "break"  # Bloquea el comportamiento predeterminado de la tecla

    def quitar_foco(root, event, entry):
        # Si el clic no es sobre el Entry, quita el enfoque
        if event.widget != entry:
            root.focus()

    
