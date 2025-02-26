#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent
from ev3dev2.sensor.lego import GyroSensor
import time

# Constantes
LADO = 30  # Longitud del lado del cuadrado en centímetros
SPEED = SpeedPercent(30)

# Función para girar 90 grados
def girar_90_grados(tank):
    tank.turn_degrees(speed=SPEED, target_angle=90 )

# Función para moverse hacia adelante
def moverse_adelante(tank):
    tank.on_for_seconds(SPEED, SPEED, 3)  # Moverse hacia adelante durante 3 segundos

# Inicializar objetos del motor y el giroscopio
tank = MoveTank(OUTPUT_B, OUTPUT_C)
tank.gyro = GyroSensor()

# Calibrar el giroscopio
tank.gyro.calibrate()
print("Angulo inicial:", tank.gyro.angle)
# Esperar a que el giroscopio se calibre completamente
while tank.gyro.calibrate():
    time.sleep(0.1)

# Recorrer el cuadrado
for _ in range(4):
    moverse_adelante(tank)  # Moverse hacia adelante (lado del cuadrado)
    time.sleep(2)
    girar_90_grados(tank)   # Girar 90 grados
    time.sleep(2)
    angle = tank.gyro.angle
    print("Angulo actual:", angle)
# Detener los motores al final
tank.stop()