# 🤖🛠️⚙️ EV3 Robot Preparation and ev3dev Configuration

Here we find the necessary elements for preparing the ev3dev operating system along with usage tests and connection to the robot for manipulation.

<details>
    <summary>🗃️ Table of Contents</summary>

- [🤖🛠️⚙️ EV3 Robot Preparation and ev3dev Configuration](#️️-ev3-robot-preparation-and-ev3dev-configuration)
  - [📝 Introduction](#-introduction)
  - [💿🔨 Creating a Bootable SD with ev3dev](#-creating-a-bootable-sd-with-ev3dev)
  - [📶📡 Connecting to the PC via Wi-Fi](#-connecting-to-the-pc-via-wi-fi)
    - [🚗🎛️ Motor Tests](#️-motor-tests)
      - [🔄🛞 Individual Motor Movement Test](#-individual-motor-movement-test)
      - [🛑🏎 Braking Test](#-braking-test)
      - [↪️🌀🚗 Robot Turn](#️-robot-turn)
      - [🐢🟡🚗 Soft Braking](#-soft-braking)
    - [📜🐍 Python Test Scripts](#-python-test-scripts)
      - [📂🧪🔬 Creating the Test Directory](#-creating-the-test-directory)
      - [🚀💡 First Execution Test](#-first-execution-test)
      - [🔄◻️🏁 Square Trajectory](#️-square-trajectory)
      - [🕵️‍♂️🎮 Test with PS4 Controller](#️️-test-with-ps4-controller)

</details>

## 📝 Introduction

EV3Dev is a Linux-based operating system designed to run on the LEGO Mindstorms EV3, providing a more flexible and powerful environment than the original firmware. It allows developers to use programming languages such as Python, C++, Java, and others.

In this section, we will follow all the steps to configure the ev3dev operating system along with details and recommendations for its use.

>[!NOTE]
>If you want to know more about the ev3dev operating system, you can check its [official page](https://www.ev3dev.org/) and to learn what other programming languages you can use, check the [programming languages](https://www.ev3dev.org/docs/programming-languages/) section.

## 💿🔨 Creating a Bootable SD with ev3dev

You must create a bootable SD so it loads the ev3dev system. Then, we will connect to the robot using an SSH connection to manipulate the files. The SSH connection can be done via cable, Bluetooth, Ethernet, or Wi-Fi. 

>[!TIP]
>I recommend using a Wi-Fi connection since it is the most stable and you won’t have cable problems.

> [!IMPORTANT]
>To use the ev3dev system you need an SD card with at least 2 GB of storage.

To choose a compatible SD and a Wi-Fi adapter, it is recommended to read the following pages:
* [Selecting an SD](https://github.com/ev3dev/ev3dev/wiki/Selecting-a-microSD-card)
* [Wi-Fi adapters compatible with leJos](https://lejosnews.wordpress.com/2015/02/03/comparing-wifi-adapters/)
* [Wi-Fi adapters compatible with ev3dev](https://github.com/ev3dev/ev3dev/wiki/USB-Wi-Fi-Dongles)

Keep in mind that the "EV3 Brick" has several processing and compatibility limitations, so it is important to verify that what you are buying works with the robot.

>[!NOTE]
>It should be clarified that this is a boot from a different storage unit, so the original firmware of the EV3 brick is not affected or modified.

Once you have the SD, follow the steps on the ev3dev page [Bootable SD](https://www.ev3dev.org/docs/getting-started/). Insert the SD into the robot and turn it on to boot from it (if you are using the Wi-Fi antenna, connect it before turning on the robot).

## 📶📡 Connecting to the PC via Wi-Fi

For this connection, you can either manually configure the Wi-Fi network or set it up from the PC using a [Bluetooth](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/) or [USB](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/) connection. Once configured, we can connect to the robot from the PC using an [SSH](https://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/) connection. To do this, we will open a terminal and run the following command:

```sh
ssh robot@<Robot IP Address>
```

>[!NOTE]
>The IP address assigned to the robot can be seen at the top left of the robot's screen, and the password is "maker". You can also use the command ```ssh robot@ev3dev.local ``` but if there are other robots connected or due to DNS settings of the Wi-Fi network, it may cause errors.

### 🚗🎛️ Motor Tests

ou can test some commands on the robot to verify motor functionality from the terminal.

>[!IMPORTANT]
>To ensure the commands work properly, make sure the motors are connected to ports B and C. These tests are done at 50% of the motors' maximum speed.


#### 🔄🛞 Individual Motor Movement Test

```sh
python3 -c "from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C; LargeMotor(OUTPUT_B).on_for_seconds(speed=50, seconds=2); LargeMotor(OUTPUT_C).on_for_seconds(speed=50, seconds=2)"
```

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/4514641b-869f-43b0-8adf-74ec17cf0142


#### 🛑🏎 Braking Test

```sh
python3 -c "from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank; tank_drive = MoveTank(OUTPUT_B, OUTPUT_C); tank_drive.on_for_seconds(left_speed=50, right_speed=50, seconds=5, brake=True)"
```

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/5100ec6d-13a1-4fb5-8574-61f7fa2af7d3


#### ↪️🌀🚗 Robot Turn

```sh
python3 -c "from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank; tank_drive = MoveTank(OUTPUT_B, OUTPUT_C); tank_drive.on_for_seconds(left_speed=50, right_speed=45, seconds=5, brake=True)"
```

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/6e06f705-b825-4c8d-ac69-6b6de09b7f5b


#### 🐢🟡🚗 Soft Braking

```sh
python3 -c "from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank; tank_drive = MoveTank(OUTPUT_B, OUTPUT_C); tank_drive.on_for_seconds(left_speed=50, right_speed=45, seconds=5); tank_drive.off(brake=True)"
```

### 📜🐍 Python Test Scripts

#### 📂🧪🔬 Creating the Test Directory

In the robot's terminal, we will create the working directories for our Python scripts with the following commands:

```sh
cd ~
mkdir -p tests/python/Mov
```

#### 🚀💡 First Execution Test
Now we will copy the initial script, which will change the LEDs color and move both motors at 75% speed for 10 rotations.

[python_hello.py](./Scripts/pruebas/python_hello.py)

Copy the file to the robot's directory:

```sh
scp pythonHello.py robot@<Robot IP Address>:/home/robot/tests/python/Mov/
```

To run the script from the robot's terminal, give it the necessary permissions and execute it:

```sh
cd ~/tests/python/Mov/
chmod u+x pythonHello.py
./pythonHello.py #another execution option is python3 pythonHello.py
```

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/9ceeae43-7512-4ca5-8dd9-0cdb3c182c99


#### 🔄◻️🏁 Square Trajectory

Another test that can be executed is following a square trajectory.

[cuadrado.py](./Scripts/pruebas/cuadrado.py)

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/584d0fcd-5021-4c59-8e6e-98d7026d1675

In this test, it is worth noting several things: first, as seen in the video, when turning, a yaw occurs since the movement has an internal PID control that corrects when the rotation target is exceeded. Likewise, we can see that the turning movement has a degree of error which, according to the library documentation, is about 2 degrees. If turn errors are not accounted for, they accumulate to the point that sometimes a square is not formed but rather a rhombus or even an open shape.


#### 🕵️‍♂️🎮 Test with PS4 Controller

Another interesting test is the ev3dev PS4Explor3r project for remote control with a PS4 controller [PS4Explor3r](https://www.ev3dev.org/projects/2018/09/02/PS4Explor3r/).

https://github.com/JSDaleman/Robotica-movil-Lab2/assets/70998067/f3be589d-fb43-42f0-85e0-a6480df9a6db

In this test, we can teleoperate the robot with a PS4 controller by assigning commands to the buttons and joysticks for robot control.

