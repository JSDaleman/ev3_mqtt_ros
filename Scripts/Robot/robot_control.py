#!/usr/bin/env python3

"""
Modulo para el manejo 
de diferentes tipos de robots creados con el ev3 
con diferentes condiciones de motores sensores y construcción.
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
import sys
import time
import ev3dev2.motor as motor
import ev3dev2.sensor as sensor
from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent, MediumMotor, SpeedRPM
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.wheel import EV3EducationSetTire


class RobotControl:
    def __init__(self):
        self.sound = Sound()
        self.leds = Leds()

    def connect_peripheral(self, peripheral_class, *args):
        """Intenta conectar un periférico y maneja errores en caso de fallo."""
        try:
            return peripheral_class(*args)
        except Exception as e:
            print("Error al inicializar {}: {}".format(peripheral_class.__name__, e))
            sys.exit(1)


class DifferentialDrive(RobotControl):
    """
    Clase para controlar un robot de tracción diferencial.

    Motores:
        - OUTPUT_B: Motor derecho
        - OUTPUT_C: Motor izquierdo
    Sensores:
        - GyroSensor: Sensor giroscópico en un puerto LEGO EV3
    """

    def __init__(self):
        super().__init__()

        #Se inicializan los motores y el giroscopio
        self.tank = self.connect_peripheral(MoveTank, OUTPUT_B, OUTPUT_C)
        self.tank.gyro = self.connect_peripheral(GyroSensor)

        self.gyro = self.connect_peripheral(GyroSensor)

        # Calibrar el giroscopio
        self.tank.gyro.calibrate()
        print("Gyrosensor calibrating ... ")

        # Esperar a que el giroscopio se calibre completamente
        while self.tank.gyro.calibrate():
            time.sleep(0.1)
        print("GyroSensor is calibrated")

        # Definir el tipo de llanta usado
        self.llanta = EV3EducationSetTire()

        #Tiempo de funcionamiento 
        self.seconds = 0.2
        self.speed = 30


    def drive(self, left_speed, right_speed):
        #Funcion para mover el robot segun una condición de velocidad de giro o de avance/retroceso
        
        #Se intenta usar las velocidades dadas en caso de estar fuera del rango se le informa al usuario 
        try:

            if abs(left_speed) > 600 or abs(right_speed) > 600:
                raise ValueError("Las velocidades deben estar en el rango de -100 a 100.")

            brake = left_speed == -right_speed  # Frenar si es giro en el sitio
            #Frenado
            self.tank.left_motor._set_brake(brake)
            self.tank.right_motor._set_brake(brake)

            self.tank.on(SpeedRPM(left_speed), SpeedRPM(right_speed))
            

        except ValueError as e:
            print("Error en la velocidad: {}".format(e))

    def stop(self):
        #Función para parar cualquier movimiento
        self.tank.stop()
        self.motor_a.stop()

    def quit(self):
        #Función para salir de la rutina parando todos los movimientos
        self.tank.stop()
        print("Quit to the routing")
        Leds().set_color("LEFT", "BLACK")
        Leds().set_color("RIGHT", "BLACK")

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
        self.tank.stop()
        self.running = False
        self.sound.speak('Goodbye')
        Leds().set_color("LEFT", "BLACK")
        Leds().set_color("RIGHT", "BLACK")

    def interrupt(self):
        self.sound.speak('Goodbye, See you later')


class DifferentialDriveWithArm(RobotControl):
    """
    Clase para controlar un robot de tracción diferencial.

    Motores:
        - OUTPUT_B: Motor derecho
        - OUTPUT_C: Motor izquierdo
        - OUTPUT_A: Motor mediano
    Sensores:
        - GyroSensor: Sensor giroscópico en un puerto LEGO EV3
    """
    def __init__(self):
        super().__init__()
        self.motor_a = self.connect_peripheral(motor.MediumMotor, 'outA')

    def arm_down(self):
        #Funcion para bajar el brazo
        self.motor_a.run_to_abs_pos(position_sp=0, speed_sp=self.speed, stop_action="hold")

    def arm_up(self):
        #Función para subir el brazo
        self.motor_a.run_to_abs_pos(position_sp=140, speed_sp=self.speed, stop_action="hold")