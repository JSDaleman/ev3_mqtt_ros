# 🤖🛠️⚙️ Preparacion de robot ev3 y configuración de ev3dev

Aca encontramos elementos necesatios para la preparación del sistema operativo ev3dev junto a pruebas de uso y conexión al robot para su manipulación.

<details>
    <summary>Tabla de Contenidos</summary>

- [🤖🛠️⚙️ Preparacion de robot ev3 y configuración de ev3dev](#️️-preparacion-de-robot-ev3-y-configuración-de-ev3dev)
  - [📝 Introducción](#-introducción)
  - [💿🔨 Creación de SD booteable con ev3dev](#-creación-de-sd-booteable-con-ev3dev)
  - [📶📡 Conexión al PC via wifi](#-conexión-al-pc-via-wifi)
    - [🚗🎛️ Pruebas de motores](#️-pruebas-de-motores)
      - [🔄🛞 Prueba movimiento de cada motor](#-prueba-movimiento-de-cada-motor)
      - [🛑🏎 Prueba con frenado](#-prueba-con-frenado)
      - [↪️🌀🚗 Giro del robot](#️-giro-del-robot)
      - [🐢🟡🚗 Frenado suave](#-frenado-suave)
    - [📜🐍 Scripts de prueba con python](#-scripts-de-prueba-con-python)
      - [📂🧪🔬 Creación de directorio de pruebas](#-creación-de-directorio-de-pruebas)
      - [🚀💡 Primera prueba de ejecución](#-primera-prueba-de-ejecución)
      - [🔄◻️🏁 Trayectoria de un cuadrado](#️-trayectoria-de-un-cuadrado)
      - [🕵️‍♂️🎮 Prueba con control de PS4](#️️-prueba-con-control-de-ps4)

</details>

## 📝 Introducción

EV3Dev es un sistema operativo basado en Linux diseñado para ejecutarse en el LEGO Mindstorms EV3, proporcionando un entorno más flexible y potente que el firmware original. Permite a los desarrolladores utilizar lenguajes de programación como Python, C++,Java y entre otros.

Es asi que en este apartado seguiremos todos los pasos para configurar el sistema operativo ev3dev junto a detalles y recomendaciones en su uso.

>[!NOTE]Saber más de ev3dev
Si quieres saber más del sistema operativo ev3dev puedes consultar su [pagina oficial](https://www.ev3dev.org/) y para conocer que otros lenguajes de programación puedes usar puedes consultar su apartado de [lenguajes de programación](https://www.ev3dev.org/docs/programming-languages/).

## 💿🔨 Creación de SD booteable con ev3dev

Se debe crear una SD booteable para que cargue el sistema ev3dev luego nos conectaremos al robot mediante una conexión ssh al sistema del robot para manipular los archivos. La conexión ssh se puede hacer por cable, bluethoot, ethernet o wifi. 

>[!TIP]
Te recomiendo usar la conexión wifi dado que es la más estable y no tienes pobrlemas con cables.

> [!IMPORTANT]Importante
Para poder utilizar el sistema ev3dev se necesita tener una memoria SD de minimo 2 GB de alamacenamiento.

Para elegir una SD compatible y un adaptador wifi se recomienda leer las siguientes paginas:
* [Seleccion de SD](https://github.com/ev3dev/ev3dev/wiki/Selecting-a-microSD-card)
* [Antenas wifi compatibles leJos](https://lejosnews.wordpress.com/2015/02/03/comparing-wifi-adapters/).
* [Antena wifi compatibles con ev3dev](https://github.com/ev3dev/ev3dev/wiki/USB-Wi-Fi-Dongles)

Ten presente que el "EV3 Brick" tiene varias limitantes de procesamiento y de compatibilidad por lo cual es importante verificar que vas a comprar que sea funcional con el robot.

>[!NOTE]Aclaración
Acabe aclarar que este es un booteo por una unidad de almacenamiento diferente por lo cual no se afecta o modifica el firmware original que posee el bloque ev3.

Una vez se tiene la SD se pueden seguir los paso de la pagina de ev3dev [SD booteable](https://www.ev3dev.org/docs/getting-started/). Se debe poner en el robot la SD y encenderlo para que boote por esta (Si usas la antena wifi tambien conectala antes de inicar el robot).


## 📶📡 Conexión al PC via wifi

Para esta conexión se puede hacer por dos vias la primera es configurar manualmente la red wifi a la cual se conectara o configurandola por medio del pc por conexión [bluethoot](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/) o [USB](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/). Una vez configurada nos podremos conectar al robot atravez de esta en el PC usando una conexión [SSH](https://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/).Para esto lanzaremos una terminal y mandaremos el siguente comando

```sh
ssh robot@<Dirección IP del robot>
```
>[!NOTE]Nota
 La dirrección IP asignada al robot se puede ver en la parte superior a la izquierda del robot y el password es "maker" se puede usar tambien el comado ```ssh robot@ev3dev.local ``` pero al habero otros robots conectados o por configuración DNS de la red wifi puede generar algún error.

### 🚗🎛️ Pruebas de motores

Se pueden probar unos comandos en el robot para verificar el funcionamiento de motores por el terminal.

>[!IMPORTANT] Importante
Para que los comandos funcionen adecuadamente asegurese que los motores esten en los puertos B y C. Estas pruebas se realizan a velocidad del 50% de la velocidad máxima de los motores.

#### 🔄🛞 Prueba movimiento de cada motor

```sh
python3 -c "from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C; LargeMotor(OUTPUT_B).on_for_seconds(speed=50, seconds=2); LargeMotor(OUTPUT_C).on_for_seconds(speed=50, seconds=2)"
```

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/4514641b-869f-43b0-8adf-74ec17cf0142

#### 🛑🏎 Prueba con frenado

```sh
python3 -c "from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank; tank_drive = MoveTank(OUTPUT_B, OUTPUT_C); tank_drive.on_for_seconds(left_speed=50, right_speed=50, seconds=5, brake=True)"
```

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/5100ec6d-13a1-4fb5-8574-61f7fa2af7d3

#### ↪️🌀🚗 Giro del robot
```sh
python3 -c "from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank; tank_drive = MoveTank(OUTPUT_B, OUTPUT_C); tank_drive.on_for_seconds(left_speed=50, right_speed=45, seconds=5, brake=True)"
```


https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/6e06f705-b825-4c8d-ac69-6b6de09b7f5b


#### 🐢🟡🚗 Frenado suave
```sh
python3 -c "from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank; tank_drive = MoveTank(OUTPUT_B, OUTPUT_C); tank_drive.on_for_seconds(left_speed=50, right_speed=45, seconds=5); tank_drive.off(brake=True)"

```

### 📜🐍 Scripts de prueba con python

#### 📂🧪🔬 Creación de directorio de pruebas

En la terminal del robot vamos a crear los directorios de trabajo para nuestros scripts de python con los siguentes comandos:

```sh
cd ~
mkdir -p pruebas/python/Mov
```

#### 🚀💡 Primera prueba de ejecución

Ahora copiaremos el scritp inicial el cual cambiara los leds de color y movera en los dos motores con velocidad del 75% por 10 rotaciones.

[python_hello.py](./Scripts/pruebas/python_hello.py)

Copiaremos el archivo en el directorio del robot 

```sh
scp pythonHello.py robot@<Dirección IP del robot>:/home/robot/pruebas/python/Mov/
```

Para correr el script en la terminar del robot le daremos los permisos necesarios para ejecutar el archivo y lo correremos

```sh
cd ~/pruebas/python/Mov/
chmod u+x pythonHello.py
./pythonHello.py #otra opcion de ejecucion es python3 pythonHello.py
```

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/9ceeae43-7512-4ca5-8dd9-0cdb3c182c99


#### 🔄◻️🏁 Trayectoria de un cuadrado

Otra prueba que se puede ejecutar es la de seguir una trayectoria de un cuadrado.

[cuadrado.py](./Scripts/pruebas/cuadrado.py)

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/584d0fcd-5021-4c59-8e6e-98d7026d1675

En esta prueba cabe resaltar varias cosas en esta prueba la primera es que como se ve en el video al momento de girar sucede una guiñada ya que el movimiento tiene un control PID interno el cual corrige el movimiento cuando se pasa de la rotación objetivo. Asimismo podemos ver que el movimiento de girar posee un grado de error que si se revisa la documentación de la libreria se puede encontara que es de 2 grados si no se declara los errores de giros se van acumulando a un grado tal que no se hace un cuadrado en algunas ocaciones sino una especie de rombo o en otros una figura abierta.

#### 🕵️‍♂️🎮 Prueba con control de PS4

Otra prueba interesante es la prueba del proyecto de ev3dev PS4Explor3r para control remoto con un control de PS4 [PS4Explor3r](https://www.ev3dev.org/projects/2018/09/02/PS4Explor3r/).

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/f3be589d-fb43-42f0-85e0-a6480df9a6db

En esta prueba podemos teleoperar el robot con un control de PS4 asignando comandos a los botones y joysticks para el manejo del robot.