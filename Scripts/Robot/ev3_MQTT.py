#!/usr/bin/env python3

"""
Modulo para el manejo 
de diferentes tipos de robots creados con el ev3 
con diferentes condiciones de motores sensores y construcción.
Usando MQTT para la comunicación con el PC
"""
__author__ = "Juan Sebastian Daleman Martinez"
__copyright__ = "Copyright 2025, Ev3 ROS atravez de MQTT"
__credits__ = ["David Fisher"]
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Juan Sebastian Daleman Martinez"
__email__ = "jdaleman@unal.edu.co"
__status__ = "Development"

#Impotación de las librerias necesarias
from ev3dev2.led import Leds
import mqtt_remote_method_calls as com
import robot_delegate as delegate

#Se inicial el main
if __name__ == '__main__':
    try:
        #Impresión de que se ha iniciado el robot y se ponen los leds en rojo
        print("Start robot")
        Leds().set_color("LEFT", "RED")
        Leds().set_color("RIGHT", "RED")

        #Se crea el delegado de recepción de mensajes MQTT y se ponen los leds en amber
        ev3_delegate = delegate.Ev3DelegateDiffDrive()
        mqtt_client = com.MqttClient(ev3_delegate)
        Leds().set_color("LEFT", "AMBER")
        Leds().set_color("RIGHT", "AMBER")

        #Se declara el cliente mqtt como el cliente que usara el delegado
        ev3_delegate.setmqtt_client(mqtt_client)

        #Se conecta al topico para sucricón y publicacion con el PC y se poenen los leds en verde
        mqtt_client.connect_to_pc()
        Leds().set_color("LEFT", "GREEN")
        Leds().set_color("RIGHT", "GREEN")

        #Se crea el bulce infinito de funcionamiento
        ev3_delegate.loop_forever()
        print("Shutdown complete")
        mqtt_client.close()

    except KeyboardInterrupt:
        ev3_delegate.interrupt_close()
        mqtt_client.close()
