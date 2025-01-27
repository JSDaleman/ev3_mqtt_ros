#!/usr/bin/env python3

__author__ = "Juan Sebastian Daleman Martine"
__copyright__ = "Copyright 2025, Ev3 ROS atravez de MQTT"
__credits__ = ["David Fisher"]
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Juan Sebastian Daleman Martine"
__email__ = "jdaleman@unal.edu.co"
__status__ = "Development"

#Creación de la clase personalizada para la recepción de mensajes MQTT
class PcDelegate(object):

    """ Los metodos de esta clase seran los que procesen los mensajes MQTT recibidos
        los atributos seran elementos de control necesarios en el procesamiento """

    def __init__(self):

        #label donde se presentara los datos de orientación dado por el giro sensor
        self.label = None

    def setlabel(self,label):
        #Función para declaración de label que se usara para datos del giro sensor
        self.label = label

    def print_message(self, message):
        #Función para procesamiento de mensaje recibido de tipo "print_message"

        #Impression del mesaje recibido
        print("Message received:", message)

    def Angle(self, angle):
        #Función para procesamiento de mensaje recibido de tipo "Angle"

        #Se pone el angulo en convencion anti-horaria
        angle = angle*-1
        #Actualización del label de presentación e impresion del angulo recibido
        self.label.config(text=str(angle))
        print("Angle received:", angle)