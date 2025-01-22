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
import tkinter
from tkinter import ttk
import app.GUI.styles.styles as styles
import app.MQTT.mqtt_remote_method_calls as com
import app.MQTT.delegate as delegate


#Función de creación de GIU
def GUI():

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

    StyleButton = styles.StyleButton(root)  # Acceder a la clase a través de GUI.styles.styles
    StyleButton.apply_style(angle_button)
    StyleButton.apply_style(forward_button)
    StyleButton.apply_style(left_button)
    StyleButton.apply_style(stop_button)
    StyleButton.apply_style(right_button)
    StyleButton.apply_style(back_button)
    StyleButton.apply_style(up_button)
    StyleButton.apply_style(down_button)
    StyleButton.apply_style(q_button)
    StyleButton.apply_style(e_button)

    StyleFrame = styles.StyleFrame(root)  # Acceder a la clase a través de GUI.styles.styles
    StyleFrame.apply_style(main_frame)

    Stylelabel = styles.StyleLabel(root)  # Acceder a la clase a través de GUI.styles.styles
    Stylelabel.apply_style(left_speed_label)
    Stylelabel.apply_style(right_speed_label)
    Stylelabel.apply_style(angle_label)
    Stylelabel.apply_style(angle_value_label)

    StyleEntry = styles.StyleEntry(root)  # Acceder a la clase a través de GUI.styles.styles
    StyleEntry.apply_style(left_speed_entry)
    StyleEntry.apply_style(right_speed_entry)

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

    #Cración de delegado para mensajes MQTT y cliente MQTT
    my_delegate = delegate.PcDelegate()
    mqtt_client = com.MqttClient(my_delegate)

    #Creación de suscripcion a topico MQTT LEGOEV301/msgPC y publicacion en topico  LegoEV301/msgLegoEv3
    mqtt_client.connect_to_ev3()
    
    #Llamado a GIU
    GUI()

    #Cerrado del cliente MQTT
    mqtt_client.close()
    