# ev3dev_ROS
Integración de la plataforma robotica Lego mindstorm EV3 con ROS a traves de comunicación MQTT
Autor: Juan Sebastian Daleman

Tabla de Contenidos
---

- [Conexión Lego EV3 con ROS](#conexi%C3%B3n-lego-ev3-con-ros).
- [Preparación de entorno e intalacion de librerias y paquetes](#preparación-de-entorno-e-intalacion-de-librerias-y-paquetes).
  - [Creacion del workspace](#creacion-del-workspace).
  - [Instalacion de libreria de python](#instalacion-de-libreria-de-python)
- [Creación de SD booteable con ev3dev](#creación-de-sd-booteable-con-ev3dev)
- [Conexión al PC via wifi](#conexión-al-pc-via-wifi)
  - [Pruebas de motores](#pruebas-de-motores)
  - [Scripts de prueba con python](#scripts-de-prueba-con-python)
- [Comunicación mqtt](#comunicación-mqtt)
- [Implementación de la comunicación](#implementación-de-la-comunicación)
  - [Creación de broker y modificación de archivos](#creación-de-broker-y-modificación-de-archivos)
  - [Carga de archivos al robot](#carga-de-archivos-al-robot)
  - [Compilación del paquete](#compilación-del-paquete)
- [Ejecución](#ejecucion)
- [Referencias](#Referencias).

## Conexión Lego EV3 con ROS

Para generar la conexión se hara a traves de comunicación mqtt e implementación de codigo en python para esto 

## Preparación de entorno e intalacion de librerias y paquetes

### Creacion del workspace

Para esto crearemos un directrotio que sera nuestro workspace y tendra nuestros archivos de intalación

```
cd ~
mkdir ev3dev_ros
cd ev3dev_ros
mkdir src
cd src
catkin_create_pkg ev3dev_ros
```

### Instalacion de libreria de python

Para la instalacion de la libreria en python descargaremos los archivos necesarios y haremos la instalcion con los siguientes comandos

```
cd ~
mkdir librerias
cd ~/librerias/
git clone https://github.com/ev3dev/ev3dev-lang-python.git
cd ~/librerias/ev3dev-lang-python
sudo python3 setup.py install
```


## Creación de SD booteable con ev3dev
Para poder conectar el lego EV3 con ROS primero se necesita tener una memoria SD de minimo 2 GB de alamacenamiento y una antena USB wifi para el robot EV3. Para elegir una SD compatible y un adaptador wifi se recomienda leer las siguientes paginas:
* [Seleccion de SD](https://github.com/ev3dev/ev3dev/wiki/Selecting-a-microSD-card)
* [Antenas wifi compatibles leJos](https://lejosnews.wordpress.com/2015/02/03/comparing-wifi-adapters/).
* [Antena wifi compatibles con ev3dev](https://github.com/ev3dev/ev3dev/wiki/USB-Wi-Fi-Dongles)

  Para acceder a la programación del robot EV3 por una API diferente a la de lego usamos un booteo de una distribución de Linux Debian desarrollada para el robot conocido como [ev3dev](https://www.ev3dev.org/) este fue desarrollado para el uso de diferentes lenguajes de programación con el robot ev3 como python, micropython, java, C++, C y etc. (Para conocer todos los lenguajes disponibles ver [lenguajes de programación](https://www.ev3dev.org/docs/programming-languages/)).

  **Nota:** Acabe aclarar que este es un booteo por una unidad de almacenamiento diferente por lo cual no se afecta o modifica el firmware original que posee el bloque ev3.
  
  Para crear la SD booteable se siguieron los pasos de la pagina de ev3dev [SD booteable](https://www.ev3dev.org/docs/getting-started/). Una vez con la antena colocada en el robot y la SD se prende este y se espera que se inicialice el sistema.

## Conexión al PC via wifi
Para esta conexión se puede hacer por dos vias la primera es configurar manualmente la red wifi a la cual se conectara o configurandola por medio del pc por conexión [bluethoot](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/) o [USB](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/). Una vez configurada nos podremos conectar al robot atravez de esta en el PC usando una conexión [SSH](https://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/).Para esto lanzaremos una terminal y mandaremos el siguente comando

```
ssh robot@<Dirección IP del robot>
```
**Nota:** La dirrección IP asignada al robot se puede ver en la parte superior a la izquierda del robot y el password es "maker" se puede usar tambien el comado ```ssh robot@ev3dev.local ``` pero al habero otros robots conectados o por configuración DNS de la red wifi puede generar algún error.

### Pruebas de motores
Si desea probar el funcionamiento de motores por el terminal puede conectar los motores en los puestos B y C del robot y corra el siguente comando el cual movera las dos ruedas con una velocidad de 50 grados/s sin frenado premero la del motor conectado al puerto C y luego la del motor conectado al puerto C.

* Prueba movimiento de cada motor
```
python3 -c "from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C; LargeMotor(OUTPUT_B).on_for_seconds(speed=50, seconds=2); LargeMotor(OUTPUT_C).on_for_seconds(speed=50, seconds=2)"
```

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/4514641b-869f-43b0-8adf-74ec17cf0142

* Prueba con frenado
```
python3 -c "from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank; tank_drive = MoveTank(OUTPUT_B, OUTPUT_C); tank_drive.on_for_seconds(left_speed=50, right_speed=50, seconds=5, brake=True)"
```

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/5100ec6d-13a1-4fb5-8574-61f7fa2af7d3

* Giro del robot
```
python3 -c "from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank; tank_drive = MoveTank(OUTPUT_B, OUTPUT_C); tank_drive.on_for_seconds(left_speed=50, right_speed=45, seconds=5, brake=True)"
```


https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/6e06f705-b825-4c8d-ac69-6b6de09b7f5b


* Frenado suave
```
python3 -c "from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank; tank_drive = MoveTank(OUTPUT_B, OUTPUT_C); tank_drive.on_for_seconds(left_speed=50, right_speed=45, seconds=5); tank_drive.off(brake=True)"

```


### Scripts de prueba con python
En la terminal del robot vamos a crear los directorios de trabajo para nuestros scripts de python con los siguentes comandos

```
cd ~
mkdir pruebas
cd pruebas/
mkdir python
cd python/
mkdir Mov
cd Mov
```

ahora en crearemos el scritp inicial el cual lo que hara es que cambiara los leds de color y movera en los dos motores con velocidad del 75% por 5 rotaciones

[pythonHello.py](https://github.com/JSDaleman/Robotica-movil-Lab2/blob/Cambios-lab2/Scripts/Mov/pythonHello.py)

copiaremos el archivo en el directorio del robot 

```
scp pythonHello.py robot@<Dirección IP del robot>:/home/robot/pruebas/python/Mov/
```

Para correr el script en la terminar del robot le daremos los permisos necesarios al archivo y lo correremos
```
cd ~/pruebas/python/Mov/
chmod +x pythonHello.py
python3 pythonHello.py
```

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/9ceeae43-7512-4ca5-8dd9-0cdb3c182c99


Otro script que se puede usar para hacer pruebas es el siguiente para una trayectoria de un cuadrado [Cuadrado.py](https://github.com/JSDaleman/Robotica-movil-Lab2/blob/Cambios-lab2/Scripts/Mov/Cuadrado.py) o se puede tambien probar el del poryecto de ev3dev PS4Explor3r para control remoto con un control de PS4 [PS4Explor3r](https://www.ev3dev.org/projects/2018/09/02/PS4Explor3r/)

* Cuadrado.py


https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/584d0fcd-5021-4c59-8e6e-98d7026d1675


En esta prueba cabe resaltar varias cosas en esta prueba la primera es que como se ve en el video al momento de girar sucede una guiñada ya que el movimiento tiene un control PID interno el cual corrige el movimiento cuando se pasa de la rotación objetivo. Asimismo podemos ver que el movimiento de girar posee un grado de error que si se revisa la documentación de la libreria se puede encontara que es de 2 si no se declara los errores de giros se van acumulando a un grado tal que no se hace un cuadrado en algunas ocaciones sino una especie de rombo o en otros una figura abierta.

* PS4Explor3r


https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/f3be589d-fb43-42f0-85e0-a6480df9a6db


## Comunicación mqtt

Para poder integrar el robot lego ev3 con ros se buscaron varias formas para comunicarse con ros entre las cualses se encontro la comunicación mqtt la cual sigue una estructura similar a ros donde los elementos que se comunican se conectan a un broker mqtt el cual maneja los mensajes recibios, se manejas topicos en los cuales se pueden publicar mensajes y se puden suscribir para hacer la recepción de mensajes en donde se tiene tiene una escucha permanente para recibir los mensajes dependiendo del QoS del mesnaje se puede tener QoS 0 en donde el mensaje se entrega una unica vez sin mensaje de respuesta de entraga ni almacenamiento sino es entregado se pierde, QoS 1 se asegura la recepción del mensaje se envia el mensaje tantas veces como sea necesario hasta que el receptor confirme la recepción y el QoS 2 se asegura que el mensje siempres sea recibido esperando el emisor un mensaje de confirmación de procesamiento del mensaje para eliminarlo. Las ventajas de esta comunicación es que es de mesajes pequeños con los cuales no se requiere mucho recurso de computo para procesarse, versatilidad en los mensajes y comunicación permitiendo estar conectado a diferentes topicos al tiempo y manejando canales para cada mensaje y que los mensajes controlados tengan varios datos para controlar equipos.

En esta comunicación los equipos que se conectan son conocidos como clientes del broker MQTT para crear este cliente en el PC se uso [modulo MQTT PC](https://github.com/JSDaleman/Robotica-movil-Lab2/blob/Cambios-lab2/Scripts/Parte%20B%20Ev3/ev3dev_ros/scripts/mqtt_remote_method_calls.py) y para el ev3 se creo el de [modulo MQTT EV3](https://github.com/JSDaleman/Robotica-movil-Lab2/blob/Cambios-lab2/Scripts/Parte%20B%20Ev3/Robot/mqtt_remote_method_calls.py) en donde se crean todos los elementos para la creación del cliente y las sucripción y publicación a los topicos necesarios para que se intercomunique por medio del broker, para la recepción de los mesajes en cada caso se crean delegados que según el mesaje jason recibido lo procesaran para generar acciónes en la interfaz o en el robot. Para el control del robot se creo un modulo en python [robot_control.py](https://github.com/JSDaleman/Robotica-movil-Lab2/blob/Cambios-lab2/Scripts/Parte%20B%20Ev3/Robot/robot_control.py) en el cual se tiene la clase del robot y los metodos que este puede realizar y [ev3_MQTT.py](https://github.com/JSDaleman/Robotica-movil-Lab2/blob/Cambios-lab2/Scripts/Parte%20B%20Ev3/Robot/ev3_MQTT.py) crea el cliente que estara en ejecución en el robot y el delegado correspondiente. Para el caso del PC se creo el paquete en ROS [ev3dev_ros]([ev3dev_ros](https://github.com/JSDaleman/Robotica-movil-Lab2/tree/Cambios-lab2/Scripts/Parte%20B%20Ev3/ev3dev_ros)) el cual crea el nodo que puede comunicarse con otros nodos en ROS y funciona de puente entre ROS y el broker MQTT. Es de esta forma que la estructura de la comunicación para integrar ros es la siguiente.

![Comunicaciónes](https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/ac8bc943-ea79-49ea-a248-852512709800)

## Implementación de la comunicación

### Creación de broker y modificación de archivos
Lo primero sera crear el broker MQTT para esto usaremos [hivemq](https://www.hivemq.com/) que nos permite crear un broker gratuito con un trafico maximo de 10 GB que al ser nuestros mensajes tan puqeños y bajo trafico sera más que suficiente y se pueden conectar hasta 100 sesiones al tiempo. Una vez creado iremos a la siguiente pestaña de resumen.

![image](https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/62362c28-b876-47cb-a5df-69f8fc6677b4)

De esta sacaremos los datos de Cluster URL y Port los cuales replazaremos de los archivos de  [modulo MQTT EV3](https://github.com/JSDaleman/Robotica-movil-Lab2/blob/Cambios-lab2/Scripts/Parte%20B%20Ev3/Robot/mqtt_remote_method_calls.py) y [GIU_Control](https://github.com/JSDaleman/Robotica-movil-Lab2/blob/Cambios-lab2/Scripts/Parte%20B%20Ev3/ev3dev_ros/scripts/GIU_Control.py) para poder conectarnos a nuestro propio broker. Luego iremos a la pestaña Access Management para crear el usurio con contraseña para la seguridad en este caso el usurio y contraseña seran ```LegoEV301``` el cual es el nombre del robot. El nombre dado al robot consiste de dos parte "LegoEV3" + Lego_ID que es un número de identificación que se da en los archivos anteriormente modificados para tener una identificación del robot por si deseamos conectar más robots en la red y manejarlos.

![image](https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/eb66381b-6ed9-45df-b269-845c788bce5c)

Leugo iremos a la pestaña web client en donde ingrsaremos las anteriores credenciales y conectaremos el cliente. Despues nos suscribiremos a todos los topicos para ver todo el trafico esta pestaña es util para verificar el trafico que se esta teniendo y hacer pruebas de mensajes.

![image](https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/a390c292-2093-438e-a0b7-0527c92722cd)


### Carga de archivos al robot
En la terminal de la conexión con el robot crearemos un directorio para los archivos de la conexión y que ejecutaremos mas adelante para controlarlo

```
cd ~/pruebas/python/
mkdir MQTT
cd ~/pruebas/python/MQTT
```

luego copiaremos como se ha mostrado anteriormente todos los archivos del robot

### Compilación del paquete
los archivos en la carpeta de [scripts](https://github.com/JSDaleman/Robotica-movil-Lab2/tree/Cambios-lab2/Scripts/Parte%20B%20Ev3/ev3dev_ros/scripts) los copiaremos en el paquete creado de ev3dev_ros de tal forma que quede la siguiente organización de los archivos.

![image](https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/04f98a99-03f9-4e8b-bfbe-f51418f00c04)

Ahora modiifcaremos el archivo CMakeLists.txt agregando al final de este el siguiente codigo y guardamos los coambios

```
catkin_install_python(PROGRAMS
    scripts/GIU_Control.py
    scripts/mqtt_remote_method_calls.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
    )
```

ya con todos los archivos necesarios y la modificacion compilaremos el paquete

```
cd ~/ev3dev_ros/
catkin_make
source devel/setup.bash
```

## Ejecucion 
Para la ejecución abriremos kitty y lanzaremos cuatro terminales (prar abrir las cuadro abriremos el program y opriremos tres veces ctrl + shift + enter).

* Primera terminal
  En esta haremos la conexión shh con el robot para iniciar la ejecución del cliente MQTT para el control de este recordar que la contraseña es "maker"
  ```
  ssh robot@ev3dev.local
  maker
  cd ~/pruebas/python/MQTT
  python3 ev3_MQTT.py
  ```

* Segunda terminal
  En esta iniciaremos el nodo Master de ROS
  ```
  roscore
  ```

* Tercera terminal
  En esta inicaremos el nodo de turtlesim
  ```
  rosrun turtlesim turtlesim_node
  ```

* Cuarta terminal
  En esta inicaremos nuestro nodo de ros con la GUI
  ```
  rosrun ev3dev_ros GIU_Control.py
  ```

Obteniendo lo mostrado a continuación
![Terminales](https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/948cb35b-e152-4094-8a82-10b70f5d180b)

Ya con esto se desplegara la interfaz donde el usuario puede hacer que el robot gire de un lado o a otro además poder ir a adelante o atras, subir o bajar el brazo o solicitar la orientación actual del robot y verla reflejada en la orientación de la tortuga.

![GIU](https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/2dfd4890-bb76-4eb1-9ba9-2559c0825ade)





## Referencias
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


