#!/usr/bin/env python3

"""
Modulo para el manejo 
de diferentes tipos de robots creados con el ev3 
con diferentes condiciones de motores sensores y construcción.
Usando MQTT para la comunicación con el PC
"""
__author__ = "Juan Sebastian Daleman Martine"
__copyright__ = "Copyright 2025, Ev3 ROS atravez de MQTT"
__credits__ = ["David Fisher"]
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Juan Sebastian Daleman Martine"
__email__ = "jdaleman@unal.edu.co"
__status__ = "Development"

#Impotación de las librerias necesarias
import mqtt_remote_method_calls as com
import robot_control as robot
from ev3dev2.button import Button
from ev3dev2.led import Leds
import time
import sys

#Creación de la clase personalizada para la recepción de mensajes MQTT
class MyDelegate(object):

    """ Los metodos de esta clase seran los que procesen los mensajes MQTT recibidos
        los atributos seran elementos de control necesarios en el procesamiento """
    
    def __init__(self):

        #Se crea el objeto robot de una transmisión diferencial
        self.robot = robot.DifferentialDrive()

        #Se declara el cliente mqtt como None
        self.mqtt_client = None

        #Elementos para mensajes a enviar
        self.msgtype = None
        self.msglist = None

    def setmqtt_client(self, mqtt_client):
        #Función para declara el cliente mqtt que se usara
        self.mqtt_client = mqtt_client

    def drive(self, left_speed, right_speed):
        #Función para manejar el robot en la parte de tracción
        self.robot.drive(left_speed, right_speed)

    def arm_down(self):
        #Función para bajar el brazo
        self.robot.arm_down()

    def arm_up(self):
        #Función para subir el brao
        self.robot.arm_up()

    def Stop(self):
        #Función para detener el robot
        self.robot.Stop()

    def Quit(self):
        #Función para salir de la rutina
        self.robot.Quit()
        sys.exit()
    
    def Angle(self):
        #Función para enviar el valor de engulo actaul del giro sensor

        #Se pide el valor del angulo
        angle = self.robot.orientation()

        #Se crea el mensaje a enviar con type "Angle" y parametro [angle]
        self.msgtype = "Angle"
        self.msglist = [angle]
        self.mqtt_client.send_message(self.msgtype, self.msglist)

        """Impresión de acciónn realizada, topico en donde se publica
        el mensaje y el mensaje enviado"""
        print(self.msgtype, end="\t")
        print(self.mqtt_client.publish_topic_name, end=" ")
        print(self.msglist)

    def loop_forever(self):
        #Función de funcionamiento hasta que se oprime el boton backspace del robot
        button = Button()
        while not button.backspace:
            time.sleep(0.01)

        if self.mqtt_client:
            self.mqtt_client.close()
        self.robot.shutdown()
        sys.exit()


def main():

    #Impresión de que se ha iniciado el robot y se ponen los leds en rojo
    print("Start robot")
    Leds().set_color("LEFT", "RED")
    Leds().set_color("RIGHT", "RED")

    #Se crea el delegado de recepción de mensajes MQTT y se ponen los leds en amber
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    Leds().set_color("LEFT", "AMBER")
    Leds().set_color("RIGHT", "AMBER")

    #Se declara el cliente mqtt como el cliente que usara el delegado
    my_delegate.setmqtt_client(mqtt_client)

    #Se conecta al topico para sucricón y publicacion con el PC y se poenen los leds en verde
    mqtt_client.connect_to_pc()
    Leds().set_color("LEFT", "GREEN")
    Leds().set_color("RIGHT", "GREEN")

    #Se crea el bulce infinito de funcionamiento
    my_delegate.loop_forever()
    print("Shutdown complete")

#Se inicial el main
main()
