#!/usr/bin/env python3

__author__ = "Juan Sebastian Daleman Martinez"
__copyright__ = "Copyright 2025, Ev3 ROS atravez de MQTT"
__credits__ = ["David Fisher"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Juan Sebastian Daleman Martinez"
__email__ = "jdaleman@unal.edu.co"
__status__ = "Development"

import sys
import time
import robot_control as robot
from ev3dev2.button import Button

#Creación de la clase personalizada para la recepción de mensajes MQTT
class Ev3DelegateDiffDrive(object):

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

    def stop(self):
        #Función para detener el robot
        self.robot.stop()

    def quit(self):
        #Función para salir de la rutina
        self.robot.quit()
        sys.exit()
    
    def angle(self):
        #Función para enviar el valor de engulo actaul del giro sensor

        #Se pide el valor del angulo
        angle = self.robot.orientation()

        #Se crea el mensaje a enviar con type "angle" y parametro [angle]
        self.msgtype = "angle"
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

    def interrupt_close(self):
        self.robot.interrupt()

class Ev3DelegateDiffDriveWithArm(Ev3DelegateDiffDrive):

    def __init__(self):

        #Se crea el objeto robot de una transmisión diferencial
        self.robot = robot.DifferentialDriveWithArm()

    def arm_down(self):
        #Función para bajar el brazo
        self.robot.arm_down()

    def arm_up(self):
        #Función para subir el brao
        self.robot.arm_up()

    