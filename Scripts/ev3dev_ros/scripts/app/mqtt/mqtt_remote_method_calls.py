#!/usr/bin/env python3

"""
Modulo de creación de cliente MQTT con elementos necesarios del
protocolo para uso con Robot Ev3 y PC.
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
import json
import paho.mqtt.client as paho
from collections.abc import Iterable
from paho import mqtt

class MqttClient(object):
    def __init__(self, delegate=None, ID=1, mqqt_borker_ip="e9d73965c3fe4220b51bf8e5f1365a27.s1.eu.hivemq.cloud"):
        #Dirección IP del broker MQTT usado por defecto
        self.mqtt_broker_ip_address = mqqt_borker_ip

        #Declaración de número de indentificación del robot
        self.Lego_ID = ID

        #Declaración del cliente y un delegado opcional de manejo de datos
        #Para funcionar en el Ev3 se quita la api version
        #ya que la verison que se usa en el robot de paho.mqtt.client es la 1.
        #Declaración del cliente y un delegado opcional de manejo de datos
        self.client = paho.Client(callback_api_version=paho.CallbackAPIVersion.VERSION2, client_id="", userdata=None, protocol=paho.MQTTv5)
        self.delegate = delegate

        #Declaración de topico de suscripción y publicación 
        self.subscription_topic_name = None
        self.publish_topic_name = None

        #Declaración de puerto de conexión del broker MQTT
        self.port = 8883

    def connect_to_ev3(self, mqtt_broker_ip_address=None, lego_robot_number=None):
        
        if mqtt_broker_ip_address is None:
            mqtt_broker_ip_address = self.mqtt_broker_ip_address
        if lego_robot_number is None:
            lego_robot_number = self.Lego_ID

        #Función para conectarse al Ev3
        #Sufijos para conectar el PC al Ev3
        self.connect("msgPC", "msgLegoEv3", mqtt_broker_ip_address, lego_robot_number)

    def connect_to_pc(self,  mqtt_broker_ip_address=None, lego_robot_number=None):

        if mqtt_broker_ip_address is None:
            mqtt_broker_ip_address = self.mqtt_broker_ip_address
        if lego_robot_number is None:
            lego_robot_number = self.Lego_ID

        #Función para conectarse al PC
        #Sufijos para conectar el EV3 al PC
        self.connect("msgLegoEv3", "msgPC", mqtt_broker_ip_address, lego_robot_number)

    def connect(self, subscription_suffix, publish_suffix, mqtt_broker_ip_address=None, lego_robot_number=None):

        if mqtt_broker_ip_address is None:
            mqtt_broker_ip_address = self.mqtt_broker_ip_address
        if lego_robot_number is None:
            lego_robot_number = self.Lego_ID
        
        #Declaración de ID del robot y sufijos necesarios para el topico MQTT
        Robot_name = "LegoEV3" + str(lego_robot_number).zfill(2)
        self.subscription_topic_name = Robot_name + "/" + subscription_suffix
        self.publish_topic_name = Robot_name + "/" + publish_suffix
        
        #Mensaje y codigo cuando se conecte con el broker MQTT
        self.client.on_connect = self.on_connect

        # Se habilita el TLS para conección segura
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.message_callback_add(self.subscription_topic_name, self.on_message)

        
        #Se colocan el nombre de usuario y contraseña para la conexión con el broker MQTT
        #Por razones practicas el nombre del robot sera usado como usuario y contaseña
        self.client.username_pw_set(Robot_name,  Robot_name)

        #Se genera la conexión con el broker MQTT en el puerto
        self.client.connect(mqtt_broker_ip_address, self.port)
        print("Conectando al mqtt broker {}".format(mqtt_broker_ip_address), end="")

        #Se inicia el ciclo del funcionamiento del cliente MQTT
        self.client.loop_start()

    def send_message(self, function_name, parameter_list=None):
        #Función para envio de mensajes

        #Cración de diccionario message_dict con una key "type" y valor el nombre de la función llamada
        message_dict = {"type": function_name}

        #Revisión de si se tiene lista de parametros para la función llamada 
        if parameter_list:

            #Verificación de que los parametros hayan sido ingresados esten en una estructura iterable
            if isinstance(parameter_list, Iterable):
                
                #Se agraga al diccionario una key "payload" y valor la lista de parametros
                message_dict["payload"] = parameter_list

            else:
                # Se le informa al usuario que los paramtros no estan en una lista y se corrige el error 
                print("The parameter_list {} is not a list. Converting it to a list for you.".format(parameter_list))
                message_dict["payload"] = [parameter_list]

        #Conversión del diccionario message_dict en un mensaje jason
        message = json.dumps(message_dict)

        #Publicación del mensaje en el broker con el topico de publicación 
        self.client.publish(self.publish_topic_name, message)

    
    def on_connect(self,client, userdata, flags, rc, properties=None):
        #Función de acción al realizarse cuando se genera la conexión al broker

        #Verificación de varaible de conexión
        if rc == 0:
            print(" ... Connected!")
        else:
            print(" ... Error!!!")
            #Si se presenta un error de conexión descomente la siguente linea y verique que lo causa
            """0: Connection successful
            1: Connection refused - incorrect protocol version
            2: Connection refused - invalid client identifier
            3: Connection refused - server unavailable
            4: Connection refused - bad username or password
            5: Connection refused - not authorised
            6-255: Currently unused."""
            #print("CONNACK received with code %s." % rc)
            exit()

        
        #Impresión de cual es el topico de publicación al que se conecto
        print("Publishing to topic:", self.publish_topic_name)

        #Declaración que la funcion on_subscribe es la misma de la clase cliente
        self.client.on_subscribe = self.on_subscribe

        #Suscripcion al topico declarado anteriormente
        self.client.subscribe(self.subscription_topic_name)

    def on_publish(self,client, userdata, mid, rc, properties=None):
        #Función para cuando la publicación fue exitosa

        #Cuando el mesaje qos es de confimación es exitoso se genera la siguiente impresión
        #impresión de identificardor de mensaje recibido
        print("mid: " + str(mid))

    
    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        #Función para cuando la suscripción fue exitosa

        #Si se quiere saber el grado qos y el mesaje de dentificación descomentar la siguiente linea
        #print("Subscribed: " + str(mid) + " " + str(granted_qos))

        #Impresión del topico al que se ha generado la suscripción
        print("Subscribed to topic:", self.subscription_topic_name)


    def on_message(self, client, userdata, msg):
        #Función para cuando se recibe un mensaje

        #Declaración de message con carga y decodificación del mensaje recibido
        message = msg.payload.decode()
        
        #Imprime el topico al que se asede el grado qos y el mensaje 
        #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        
        #Impresión del mensaje recibido por el servidor
        print("Received message:", message)

        #Si no se creo un delegado para mensajes no se procesa el mensaje
        #solo se retorna
        if not self.delegate:
            print("Missing a delegate")
            return

        
        #Atención al mensaje recivido y llamado a la función apropiada.
        try:
            #Se convierte el mensaje jason en un diccionario de python
            message_dict = json.loads(message)
        except ValueError:
            #Si no se puedde decodificar el mensaje se imprime el error y se retorna
            print("Unable to decode the received message as JSON")
            return

        #Se verifica que el diccionario tenga una key "type"
        if "type" not in message_dict:
            #Si no se tiene la key "type" se imprime el error y se retorna
            print("Received a messages without a 'type' parameter.")
            return
        
        #Se obtiene el valor asociado a la key "type"
        message_type = message_dict["type"]
        
        #Se verifica si el delegado creado tiene el metodo ingresado
        if hasattr(self.delegate, message_type):

            #Si existe el metodo se llama al metodo
            method_to_call = getattr(self.delegate, message_type)

            #Se asume que el usuario dio parametros correctos
            #Se verfica si se ingreso la lista de parametros 
            if "payload" in message_dict:

                #Si se tiene la lista de parametros se obtine esta
                message_payload = message_dict["payload"]
                #Se desempaqueta la lista y se ingra al metodo llamado
                attempted_return = method_to_call(*message_payload)

            else:

                #Si no se tiene lista de parametros solo se llama al metodo
                attempted_return = method_to_call()

            if attempted_return:
                #Si el metodo retorno algun valor se le informa al usuario ya que no es posible el manejo de valores retornados
                print("The method {} returned a value. That's not really how this library works." +
                      "The value {} was not magically sent back over".format(message_type, attempted_return))
        else:

            #Si no se encuentra el metodo llamado se le informa al usuario del error
            print("Attempt to call method {} which was not found.".format(message_type))

    def close(self):
        #Función para cerrar el cliente MQTT

        #Se imprime el mensaje de cierre del cliente y se cierra todos los elemenstos
        #Se declara al delegado como None
        print("Close MQTT")
        self.delegate = None
        self.client.loop_stop()
        self.client.disconnect()
