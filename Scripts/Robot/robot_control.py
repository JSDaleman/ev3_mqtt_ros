#!/usr/bin/env python3

"""
Modulo para el manejo 
de diferentes tipos de robots creados con el ev3 
con diferentes condiciones de motores sensores y construcción.
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
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent, MediumMotor
import ev3dev2.motor as motor
import ev3dev2.sensor as sensor
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.wheel import EV3EducationSetTire
import time
import sys



"""Creación de la clase personalizada para manejar un robot de tracción diferencial
Motores: 
    -Puerto_A: Motor mediano
    -Puerto_B: Motor largo
    -Puerto_C: Motor largo

Sensores:
    -Puerto_2: Giro sensor
"""
class DifferentialDrive(object):

    def __init__(self):
        
        
        #Se inicializan los motores y el giroscopio
        self.motor_a = motor.MediumMotor('outA')
        self.tank = MoveTank(OUTPUT_B, OUTPUT_C)
        self.tank.gyro = GyroSensor()
        self.gyro = GyroSensor()

        # Calibrar el giroscopio
        self.tank.gyro.calibrate()
        print("Gyrosensor calibrating ... ")

        # Esperar a que el giroscopio se calibre completamente
        while self.tank.gyro.calibrate():
            time.sleep(0.1)
        print("GyroSensor is calibrated")

        # Definir el tipo de llanta usado
        self.llanta = EV3EducationSetTire()

        #Sonido
        self.sound = Sound()

        #Tiempo de funcionamiento 
        self.seconds = 0.4
        self.speed = 30



    def drive(self, left_speed, right_speed):
        #Funcion para mover el robot segun una condición de velocidad de giro o de avance/retroceso
        
        #Se intenta usar las velocidades dadas en caso de estar fuera del rango se le informa al usuario 
        try:

            #Se verifica la condición de velocidades de giro
            if ((left_speed == (-1*right_speed)) or ((-1*left_speed) == right_speed)) :
                self.tank.on_for_seconds(left_speed, right_speed, self.seconds, brake=True, block=True)
            else:
                self.tank.on(left_speed, right_speed)

        except:

            print("Error range of speed is -100 to 100")

    def arm_down(self):
        #Funcion para bajar el brazo
        self.motor_a.run_to_abs_pos(position_sp=0, speed_sp=self.speed, stop_action="hold")

    def arm_up(self):
        #Función para subir el brazo
        self.motor_a.run_to_abs_pos(position_sp=140, speed_sp=self.speed, stop_action="hold")

    def Stop(self):
        #Función para parar cualquier movimiento
        self.tank.stop()
        self.motor_a.stop()

    def Quit(self):
        #Función para salir de la rutina parando todos los movimientos
        self.tank.stop()
        self.motor_a.stop()
        print("Quit to the routing")
        self.running = False
        Leds().set_color("LEFT", "BLACK")
        Leds().set_color("RIGHT", "BLACK")
        sys.exit()
        broke

    def orientation(self):
        #Función para dar la orientación dada por el giro sensor
        return self.gyro.angle

    def loop_forever(self):
        #Función para crear bucle de funcionamientmiento en caso que se use el robot como delegado
        self.running = True
        while self.running:
            time.sleep(0.1)

    def shutdown(self):
        #Función para apagar la rutina si el cliente MQTT se cierra
        self.sound.speak('Goodbye')
        self.running = False
        Leds().set_color("LEFT", "BLACK")
        Leds().set_color("RIGHT", "BLACK")
        sys.exit()