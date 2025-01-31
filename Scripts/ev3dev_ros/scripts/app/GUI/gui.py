#!/usr/bin/env python3

import tkinter
import app.gui.views.frames.differencial_frame as differencial_frame

class GUI(tkinter.Tk):

    def __init__(self, mqtt_client, delegate):
        super().__init__()
        self.mqtt_client = mqtt_client
        self.delegate = delegate

        #Creación de ventana principal del GIU y titulo de este
        self.title("Contol ev3 with MQTT messages")

        #Creación de frame y grid para grilla de posicion de elementos
        diff_frame = differencial_frame.DifferencialFrame(self, self.mqtt_client, delegate, padding=20)
        

if __name__ == '__main__':
    # Crear la ventana principal
    root = tkinter.Tk()
    root.title("Comportamiento de tecla Right")

    # Etiqueta de instrucción
    tkinter.Label(root, text="Escribe algo en el cuadro de texto:").pack(pady=10)

    # Crear el Entry
    entry = tkinter.Entry(root, width=30)
    entry.pack(pady=10)

    # Asignar binding para capturar la tecla Right
    #root.bind("<Right>", manejar_tecla_right)

    # Asignar binding para quitar el enfoque del Entry al hacer clic fuera
    #root.bind("<Button-1>", quitar_foco)

    # Botón para mostrar el texto ingresado
    def mostrar_texto():
        print("Texto ingresado:", entry.get())

    tkinter.Button(root, text="Mostrar Texto", command=mostrar_texto).pack(pady=10)

    # Iniciar el bucle principal
    root.mainloop()
    
