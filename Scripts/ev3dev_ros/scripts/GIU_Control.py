#!/usr/bin/env python3

"""
Nombre del programa: GIU_Control.py
Autor: Juan Sebastian Daleman Martinez
Curso: Fundamentos de robotica movil
Departamento de Ingeniería Mecánica y Mecatrónica
Universidad Nacional de Colombia - Sede Bogotá
Año: 2024-1S.

Programa para el control de un robot Ev3 usando el sistema ev3dev
a traves de una GIU para el usuario y mensajes jason por protocolo MQTT
para el manejo de motores y obtención de datos de un giro sensor.
Este programa esta basado en la serie de videos de: David Fisher 
https://www.youtube.com/watch?v=ZKR8pdr7CnI
"""

#Impotación de las librerias necesarias
import tkinter
from tkinter import ttk
import rospy
import math
from geometry_msgs.msg import Twist
import mqtt_remote_method_calls as com

#Creación de la clase personalizada para la recepción de mensajes MQTT
class MyDelegate(object):

    """ Los metodos de esta clase seran los que procesen los mensajes MQTT recibidos
        los atributos seran elementos de control necesarios en el procesamiento """

    def __init__(self):

        #label donde se presentara los datos de orientación dado por el giro sensor
        self.label = None

        #Variable de control para la actualización de la orientación del turtlesim
        self.Orientation = 0

        #Elementos para el mensaje del control de la tortuga de turtlesim
        self.cmd_vel_msg = Twist()
        self.cmd_vel_msg.linear.x = 0
        self.cmd_vel_msg.linear.y = 0

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
        
        #Declaración de velocidad angular del mensaje para el turtlesim 
        self.cmd_vel_msg.angular.z = 0

        #Verificación orientación y actualizar el valor según el valor recibido de angulo 
        if self.Orientation != angle:
            self.cmd_vel_msg.angular.z = ((angle-self.Orientation)*(math.pi/180))
            self.Orientation = angle

        # Publicación del mensaje Twist para el control de la tortuga
        turtle_vel_pub.publish(self.cmd_vel_msg)

#Función de creación de GIU
def GIU():

    #Creación de ventana principal del GIU y titulo de este
    root = tkinter.Tk()
    root.title("Contol ev3 with MQTT messages")

    #Creación de frame y grid para grilla de posicion de elementos
    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    """Creación de cuadro de texto para obtener valor de velocidad
       del motor izquierdo y etiqueta descritiva para el usuario"""
    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "100")
    left_speed_entry.grid(row=1, column=0)

    """Creación de cuadro de texto para obtener valor de velocidad
       del motor derecho y etiqueta descritiva para el usuario"""
    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "100")
    right_speed_entry.grid(row=1, column=2)

    """Creación de label para presnetar el valor de ángulo recibido y
       declaración en el objeto my_delagate del label que recibe dicho mensaje"""
    angle_label = ttk.Label(main_frame, text="Angle")
    angle_label.grid(row=0, column=3)
    angle_value_label = ttk.Label(main_frame, text="0")
    angle_value_label.grid(row=1, column=3)
    my_delegate.setlabel(angle_value_label)

    """Creación del boton y tecla para solicitar el ángulo"""
    angle_button = ttk.Button(main_frame, text="Update")
    angle_button.grid(row=2, column=3)
    angle_button['command'] = lambda: send_message_special(mqtt_client, "Angle", "angle button")
    root.bind('<a>', lambda event:send_message_special(mqtt_client, "Angle", "angle key"))

    """Creación del boton y tecla para hacer que el robot se mueva hacia el frente"""
    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: send_message_movtank(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()), "Forward button")
    root.bind('<Up>', lambda event: send_message_movtank(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()), "Forward key"))

    """Creación del boton y tecla para hacer que el robot gire a la izquierda"""
    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: send_message_movtank(mqtt_client, (-1/2)*int(left_speed_entry.get()), (1/2)*int(right_speed_entry.get()), "Left button")
    root.bind('<Left>', lambda event: send_message_movtank(mqtt_client, (-1/2)*int(left_speed_entry.get()), (1/2)*int(right_speed_entry.get()), "Left key"))

    """Creación del boton y tecla para hacer que el robot pare"""
    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: send_message_special(mqtt_client, "Stop", "Stop button")
    root.bind('<space>', lambda event: send_message_special(mqtt_client, "Stop", "Stop key"))

    """Creación del boton y tecla para hacer que el robot gire a la derecha"""
    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: send_message_movtank(mqtt_client, (1/2)*int(left_speed_entry.get()), (-1/2)*int(right_speed_entry.get()), "Right button")
    root.bind('<Right>', lambda event: send_message_movtank(mqtt_client, (1/2)*int(left_speed_entry.get()), (-1/2)*int(right_speed_entry.get()), "Right key"))

    """Creación del boton y tecla para hacer que el robot se meuva hacia atras"""
    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: send_message_movtank(mqtt_client, (-1)*int(left_speed_entry.get()), (-1)*int(right_speed_entry.get()), "Back button")
    root.bind('<Down>', lambda event: send_message_movtank(mqtt_client, (-1)*int(left_speed_entry.get()), (-1)*int(right_speed_entry.get()), "Back key"))

    """Creación del boton y tecla para hacer que el robot suba su brazo"""
    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_message_special(mqtt_client, "arm_up", "Up button")
    root.bind('<u>', lambda event: send_message_special(mqtt_client, "arm_up", "Up key"))

    """Creación del boton y tecla para hacer que el robot baje su brazo"""
    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_message_special(mqtt_client, "arm_down", "Down button")
    root.bind('<j>', lambda event: send_message_special(mqtt_client, "arm_down", "Down key"))

    """Creación del boton y tecla para hacer que el robot deje el programa"""
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = lambda: send_message_special(mqtt_client, "Quit", "Quit button")
    root.bind('<q>', lambda event: send_message_special(mqtt_client, "Quit", "Quit key"))

    """Creación del boton y tecla para salir de la GIU"""
    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = lambda: exit()
    root.bind('<e>', lambda event: exit())

    """Ciclo infinito de ejecución de la GIU"""
    root.mainloop()
    

#Funcion de envio de mensajes MQTT para mover el robot
def send_message_movtank(mqtt_client, left_speed_entry, right_speed_entry, msg):

    #Declaración de elementos de la lista de parametros
    msg_left = left_speed_entry
    msg_right = right_speed_entry

    #Declaración del tipo de mensaje y lista de parametros
    msgtype = "drive"
    msglist = [msg_left, msg_right]
    
    #Envio de mensaje tipo "drive" y mensaje con lista de parametros
    mqtt_client.send_message(msgtype, msglist)

    """Impresión de acciónn realizada, topico en donde se publica
       el mensaje y el mensaje enviado"""
    print(msg, end="\t")
    print(mqtt_client.publish_topic_name, end=" ")
    print(msgtype, msglist)


#Funcion de envio de mensajes MQTT para acciones diferentes a mover el robot
def send_message_special(mqtt_client, msg_special, msg):

    #Declaración del tipo de mensaje sin lista de parametros
    msgtype = msg_special

    #Envio de mensaje
    mqtt_client.send_message(msgtype)

    """Impresión de acciónn realizada, topico en donde se publica
       el mensaje y el mensaje enviado"""
    print(msg, end="\t")
    print(mqtt_client.publish_topic_name, end=" ")
    print(msg_special)


#ejecucón de script como principal o como modulo
if __name__ == '__main__':

    #Creación de nodo de ROS
    rospy.init_node('mqtt_to_ros_node', anonymous=True)
    #rate = rospy.Rate(10)

    #Creación de publicadores y suscriptores del nodo
    global turtle_vel_pub
    turtle_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)


    #Cración de delegado para mensajes MQTT y cliente MQTT
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)

    #Creación de suscripcion a topico MQTT LEGOEV301/msgPC y publicacion en topico  LegoEV301/msgLegoEv3
    mqtt_client.connect_to_ev3()
    
    #Llamado a GIU
    GIU()

    #Cerrado del cliente MQTT
    mqtt_client.close()
    