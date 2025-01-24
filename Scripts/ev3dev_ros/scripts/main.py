#!/usr/bin/env python3

__author__ = "Juan Sebastian Daleman Martine"
__copyright__ = "Copyright 2025, Ev3 ROS atravez de MQTT"
__credits__ = ["David Fisher"]
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Juan Sebastian Daleman Martine"
__email__ = "jdaleman@unal.edu.co"
__status__ = "Development"

#Impotación de las librerias necesarias
import app.mqtt.mqtt_remote_method_calls as com
import app.mqtt.delegate as delegate
import app.gui.gui as gui


#ejecucón de script como principal o como modulo
if __name__ == '__main__':

    #Cración de delegado para mensajes MQTT y cliente MQTT
    my_delegate = delegate.PcDelegate()
    mqtt_client = com.MqttClient(my_delegate)

    #Creación de suscripcion a topico MQTT LEGOEV301/msgPC y publicacion en topico  LegoEV301/msgLegoEv3
    mqtt_client.connect_to_ev3()
    
    #Llamado a GIU
    ros_gui = gui.GUI(mqtt_client, my_delegate)
    ros_gui.mainloop() 

    #Cerrado del cliente MQTT
    mqtt_client.close()
    