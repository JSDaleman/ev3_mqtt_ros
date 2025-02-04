#!/usr/bin/env python3

__author__ = "Juan Sebastian Daleman Martine"
__copyright__ = "Copyright 2025, Ev3 ROS a través de MQTT"
__credits__ = ["David Fisher"]
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Juan Sebastian Daleman Martine"
__email__ = "jdaleman@unal.edu.co"
__status__ = "Development"

# Importación de las librerías necesarias
import sys
from PyQt5.QtWidgets import QApplication
import app.mqtt.mqtt_remote_method_calls as com
import app.mqtt.delegate as delegate
import app.gui.gui as gui

# Ejecución del script como principal o como módulo
if __name__ == '__main__':
    
    # Creación de delegado para mensajes MQTT y cliente MQTT
    my_delegate = delegate.PcDelegate()
    mqtt_client = com.MqttClient(my_delegate)

    # Creación de suscripción a tópico MQTT LEGOEV301/msgPC y publicación en tópico LegoEV301/msgLegoEv3
    mqtt_client.connect_to_ev3()
    
    # Inicialización de la GUI con PyQt5
    app = QApplication(sys.argv)
    ros_gui = gui.GUI(mqtt_client, my_delegate)
    ros_gui.show()
    
    # Ejecutar la aplicación
    sys.exit(app.exec_())
