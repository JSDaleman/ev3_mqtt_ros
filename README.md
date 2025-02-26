# 🤖📡💻 Conexión de EV3 con ROS por medio de comunicación MQTT y el sistema ev3dev

Integración de la plataforma robotica Lego mindstorm EV3 con ROS a traves de comunicación MQTT. 

**Autor: Juan Sebastian Daleman**

<details>
  <summary>Tabla de Contenidos</summary>

---

- [🤖📡💻 Conexión de EV3 con ROS por medio de comunicación MQTT y el sistema ev3dev](#-conexión-de-ev3-con-ros-por-medio-de-comunicación-mqtt-y-el-sistema-ev3dev)
  - [⚙️💻🤖 Configuracion sistema ev3dev](#️-configuracion-sistema-ev3dev)
  - [🤖🔌🖥️ Conexión Lego EV3 con ROS](#️-conexión-lego-ev3-con-ros)
    - [🧰🏙️ Preparación del work space de ROS](#️-preparación-del-work-space-de-ros)
    - [📂🤖 Archivos para el robot](#-archivos-para-el-robot)
  - [📡🚀🔄 Comunicación mqtt](#-comunicación-mqtt)
    - [⚡📨 QoS (Quality of Service)](#-qos-quality-of-service)
    - [✅📊📡 Ventajas de la comunicación MQTT](#-ventajas-de-la-comunicación-mqtt)
    - [📤📡📥 Estructura de comunicación creada](#-estructura-de-comunicación-creada)
    - [🚀🌐🔧 Creación de broker y configuración](#-creación-de-broker-y-configuración)
    - [💻🔄🤖 Carga de archivos al robot](#-carga-de-archivos-al-robot)
  - [▶️📜🖥️ Ejecución de los programas](#️️-ejecución-de-los-programas)
  - [📚🔍 Referencias](#-referencias)
</details>

## ⚙️💻🤖 Configuracion sistema ev3dev
Para el funcinamiento de esta integración es importante generar una sd booteable junto a unas configuración dentro de esta para esto leer [Preparacion EV3](Preparacion.md)

## 🤖🔌🖥️ Conexión Lego EV3 con ROS

Para generar la conexión se hara a traves de comunicación mqtt en donde se busca tener un nodo en ROS que sera el puente de comunicación y el robot corra un script de python que permita su control atavez de la comunicación establecida.

### 🧰🏙️ Preparación del work space de ROS 

Crearemos un work space llamado ev3dev_ws en el cual tendremos nuestros paquetes de ros.

>[!NOTE]
>En el repositorio de [ev3_ros](https://github.com/JSDaleman/ev3dev_ROS?tab=readme-ov-file) encontraras los detalles de la estructuración de los paquetes para el funcionamiento de ROS y el como usarlos más a detalle.

```sh
cd ~
mkdir -p ev3dev_ws/src
cd ev3dev_ws
catkin_make #Compila el work space
```

Para no tener que estar contantemente llamando el archivo de configuración al compilar los paquetes lo sagregamos al archivo nano ~/.bashrc o ~/.zshrc en caso de que uses Zsh.

```sh
cd ~
nano ~/.bashrc #  ~/.zshrc en caso de que uses Zsh
```

Al final del archvio pondremos y guardamos.

```sh
source ~/ev3_ws/devel/setup.bash
```

Clanamos el repositorio con los paquetes de funcionamiento para ros. 

```sh
cd ev3dev_ws/src
git clone https://github.com/JSDaleman/ev3dev_ROS.git
cd ev3dev_ws
catkin_make #Compilamos el work space ya con los paquetes
```

### 📂🤖 Archivos para el robot

Para los archivos del robot primero los copiaremos en nuestro computador para luego copiarlos al robot.

```sh
cd ~
git clone https://github.com/JSDaleman/ev3_mqtt_ros
```

Para visualizar correctamente en visual las importaciones y detalles de los modulos es necesario hacer la instalación de la libreria de python para el ev3dev. Para lo que descargaremos los archivos necesarios y haremos la instalcion con los siguientes comandos:

```sh
cd ~/ev3_mqtt_ros
mkdir librerias
cd ~/librerias/
git clone https://github.com/ev3dev/ev3dev-lang-python.git
cd ~/librerias/ev3dev-lang-python
sudo python3 setup.py install
```

## 📡🚀🔄 Comunicación mqtt

MQTT (Message Queuing Telemetry Transport) es un protocolo de comunicación ligero basado en el modelo publicador/suscriptor, diseñado para transmitir datos de manera eficiente en redes con ancho de banda limitado, como en dispositivos IoT. En lugar de que los dispositivos se comuniquen directamente entre sí, utilizan un intermediario llamado broker, que gestiona la entrega de mensajes.

El modelo de comunicación se divide en tres elementos principales: publicadores, suscriptores y el broker. Un publicador es un dispositivo o aplicación que envía datos al broker publicando mensajes en un "topic" (tema específico). Por otro lado, un suscriptor es quien recibe estos mensajes, ya que se suscribe a un topic y obtiene actualizaciones en tiempo real cuando hay nueva información. El broker es el servidor que se encarga de recibir los mensajes de los publicadores y distribuirlos a todos los suscriptores correspondientes.

Una de las características clave de MQTT es su flexibilidad y fiabilidad en la entrega de mensajes. Cuenta con diferentes niveles de QoS (Quality of Service) que permiten controlar cómo se transmiten los mensajes, asegurando que lleguen correctamente en redes inestables. Además, al ser un protocolo ligero, es ideal para sistemas con recursos limitados, como microcontroladores y dispositivos embebidos. Gracias a su eficiencia y facilidad de uso, MQTT es ampliamente utilizado en aplicaciones de IoT, automatización industrial, domótica y robótica.

### ⚡📨 QoS (Quality of Service) 

Los Quality of service que se puede tener son:

- **QoS 0** en donde el mensaje se entrega una unica vez sin mensaje de respuesta de entraga ni almacenamiento sino es entregado se pierde
- **QoS 1** se asegura la recepción del mensaje se envia el mensaje tantas veces como sea necesario hasta que el receptor confirme la recepción
- **QoS 2** se asegura que el mensje siempres sea recibido esperando el emisor un mensaje de confirmación de procesamiento del mensaje para eliminarlo. 
  

### ✅📊📡 Ventajas de la comunicación MQTT

- 📦 Mensajes pequeños → Consume poco ancho de banda y requiere bajos recursos de cómputo.
- 🔄 Versatilidad → Permite enviar distintos tipos de mensajes y adaptarse a diversas aplicaciones.
- 📡 Conexión a múltiples tópicos → Un dispositivo puede suscribirse a varios temas al mismo tiempo.
- 📬 Manejo de canales → Cada mensaje puede organizarse en diferentes topics, facilitando la administración.
- ⚙️ Control de dispositivos → Los mensajes pueden contener múltiples datos para gestionar equipos de manera eficiente.

### 📤📡📥 Estructura de comunicación creada

Por las ventajas en especial por poder de procesamiento y adaptabilidad a sistemas como microcontroladores se escogio. Para poder usar este protocolo de comunicación se realizaron los siguentes pasos:

1. **Creación de los clientes mqtt:** Para que ros se comunique con el cliente se creo el paquete mqtt el cual crea el nodo de comunicación con el cliente y para el robot el modulo de mqtt el cual genera todas las partes necesarias de conexión (topicos, sucripción y publicación) y manejo de mensajes del protocolo (estructura de mensajes en formato jason y lectura de estos).
2. **Elementos de control:** Se creo el archivo en python para las acciones que puede realizar el robot y el paquete de control de ros para controlar elementos de la simulacion y del robot.
3. **Interfaz grafica:** Se creo la estructura de la interfaz que permite la teleoperacion del robot y su correspondiente paque en ROS.
4. **Simulación:** Despliegue de modelo del robot y seguimiento de comportamiento esperado del robot

![Comunicaciónes](https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/ac8bc943-ea79-49ea-a248-852512709800)


### 🚀🌐🔧 Creación de broker y configuración

Para crear el broker MQTT se uso [hivemq](https://www.hivemq.com/) que nos permite crear un broker gratuito con un trafico maximo de 10 GB que al ser nuestros mensajes tan peqeños y bajo trafico sera más que suficiente y se pueden conectar hasta 100 sesiones al tiempo. Una vez creado iremos a la siguiente pestaña de resumen.

![image](https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/62362c28-b876-47cb-a5df-69f8fc6677b4)

De esta sacaremos los datos de Cluster URL y Port los cuales se deben ingresar de los archivos de en el paquete mqtt y en el modulo mqtt para el robot para poder conectarnos a nuestro propio broker.

>[!TIP]
>En los modulos puedes cambiar los valores por defecto para no tener que estar ingresandolos

Luego iremos a la pestaña Access Management para crear el usurio con contraseña para la seguridad en este caso el usurio y contraseña seran ```LegoEV301``` el cual es el nombre del robot.

>[!NOTE]
>El nombre de cada robot consiste es "LegoEV3XX" donde las dos X se remplazan por el ID de identificación de cada robot.

![image](https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/eb66381b-6ed9-45df-b269-845c788bce5c)

Despues iremos a la pestaña web client en donde ingresaremos las anteriores credenciales y conectaremos el cliente. Despues nos suscribiremos a todos los topicos (usando "#") para ver todo el trafico que pasa por el broker con este usuario.

![image](https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/a390c292-2093-438e-a0b7-0527c92722cd)


### 💻🔄🤖 Carga de archivos al robot

En la terminal de la conexión con el robot crearemos un directorio para los archivos de la conexión y que ejecutaremos más adelante para controlarlo

```sh
cd ~/pruebas/python/
mkdir MQTT
cd ~/pruebas/python/MQTT
```

Luego copiaremos los archivos que estan en ev3_mqtt_ros/Scripts/Robot.

```sh
cd ev3_mqtt_ros/Scripts/Robot
scp -r ./* robot@<Dirección IP del robot>:/home/robot/pruebas/python/MQTT/
```

## ▶️📜🖥️ Ejecución de los programas



## 📚🔍 Referencias
* [Conexion de Lego Ev3 por medio de una raspberry pi](https://github.com/aws-samples/aws-builders-fair-projects/blob/master/reinvent-2019/lego-ev3-raspberry-pi-robot/README.MD) 
* [ROS desde el Lego Ev3](https://github.com/moriarty/ros-ev3)
* [Manajo con python ev3dev](https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/latest/)
* [Manejo de motores del Ev3 con Python](https://www.youtube.com/watch?v=j0-ATIe6pqg) 
* [Uso de sensor lidar con Ev3](https://www.youtube.com/watch?v=JX0zeYa-faM) 
* [Programacion y conexion SSH desde Visual Studio Code con Ev3](https://www.youtube.com/watch?v=uNSIOvqzAnY) 
* [Instalacion de ROS distribucion JADE en el Ev3](https://github.com/osmado/ev3dev_ros_distribution) 
* [ROS blog sobre lego Ev3](http://wiki.ros.org/Robots/EV3)
* [Conexión Ev3 y arduino](https://www.dexterindustries.com/howto/connecting-ev3-arduino/)
* [Manejo con ROS de Ev3 con C++](https://www.youtube.com/watch?v=iRQqEKYDRI4)
* [Github manejo con ROS de Ev3 con C++](https://github.com/srmanikandasriram/ev3-ros?tab=readme-ov-file)
* [Libreria de Python de ev3dev](https://github.com/ev3dev/ev3dev-lang-python)
* [Libreria de C++ de ev3dev](https://github.com/ddemidov/ev3dev-lang-cpp)
* [Comunicación MQTT ev3](https://www.youtube.com/watch?v=3bEbLf1KTK4 )
* [MQTT con python](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python)


