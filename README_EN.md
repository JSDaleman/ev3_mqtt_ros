# 🤖📡💻 Connection of Lego Mindstorms EV3 with ROS via MQTT Communication and the ev3dev System

Integration of the Lego Mindstorms EV3 robotics platform with ROS through MQTT communication.  

**Author: Juan Sebastian Daleman**

<details>
  <summary>🗃️ Table of Contents</summary>

---

- [🤖📡💻 Connection of Lego Mindstorms EV3 with ROS via MQTT Communication and the ev3dev System](#-connection-of-lego-mindstorms-ev3-with-ros-via-mqtt-communication-and-the-ev3dev-system)
  - [⚙️💻🤖 ev3dev System Configuration](#️-ev3dev-system-configuration)
  - [🤖🔌🖥️ Lego EV3 Connection with ROS](#️-lego-ev3-connection-with-ros)
    - [🧰🏙️ ROS Workspace Preparation](#️-ros-workspace-preparation)
    - [📂🤖 Files for the Robot](#-files-for-the-robot)
  - [📡🚀🔄 MQTT Communication](#-mqtt-communication)
    - [⚡📨 QoS (Quality of Service)](#-qos-quality-of-service)
    - [✅📊📡 Advantages of MQTT Communication](#-advantages-of-mqtt-communication)
    - [📤📡📥 Communication Structure Created](#-communication-structure-created)
    - [🚀🌐🔧 Broker Creation and Configuration](#-broker-creation-and-configuration)
    - [💻🔄🤖 Uploading Files to the Robot](#-uploading-files-to-the-robot)
  - [▶️📜🖥️ Running the Programs](#️️-running-the-programs)
    - [📡🎮🤖 Robot Teleoperation](#-robot-teleoperation)
    - [🧩🏙️🖥️ Application and rqt Plugin](#️️-application-and-rqt-plugin)
    - [🎮📊🤖 Teleoperation and Simulation](#-teleoperation-and-simulation)
  - [📚🔍 References](#-references)
</details>

## ⚙️💻🤖 ev3dev System Configuration
For this integration to work, it is important to create a bootable SD card along with some configuration steps. For details, see [EV3 Preparation](Preparation.md).

## 🤖🔌🖥️ Lego EV3 Connection with ROS

The connection will be established via MQTT communication. A ROS node will act as the communication bridge, while the robot will run a Python script that allows control through the established communication.

### 🧰🏙️ ROS Workspace Preparation

We will create a workspace called `ev3dev_ws` where our ROS packages will be stored.

>[!NOTE]
>In the [ev3_ros](https://github.com/JSDaleman/ev3dev_ROS?tab=readme-ov-file) repository, you will find details about the package structure for ROS operation and how to use them in more detail.

```sh
cd ~
mkdir -p ev3dev_ws/src
cd ev3dev_ws
catkin_make # Compile the workspace
```

To avoid constantly sourcing the setup file when compiling packages, add it to your ~/.bashrc file or ~/.zshrc if using Zsh.

```sh
cd ~
nano ~/.bashrc # Or ~/.zshrc if using Zsh
```

At the end of the file, add and save:

```sh
source ~/ev3_ws/devel/setup.bash
```

Clone the repository with the ROS packages:

```sh
cd ev3dev_ws/src
git clone https://github.com/JSDaleman/ev3dev_ROS.git
cd ev3dev_ws
catkin_make # Compile the workspace with the packages
```

### 📂🤖 Files for the Robot

First, copy the necessary files to your computer and then to the robot.

```sh
cd ~
git clone https://github.com/JSDaleman/ev3_mqtt_ros
```

To properly visualize imports and module details in Visual Studio Code, install the Python library for ev3dev:

```sh
cd ~/ev3_mqtt_ros
mkdir librerias
cd ~/librerias/
git clone https://github.com/ev3dev/ev3dev-lang-python.git
cd ~/librerias/ev3dev-lang-python
sudo python3 setup.py install
```

## 📡🚀🔄 MQTT Communication

MQTT (Message Queuing Telemetry Transport) is a lightweight communication protocol based on the publisher/subscriber model, designed for efficient data transmission over bandwidth-limited networks, such as IoT devices. Instead of communicating directly, devices use an intermediary called a broker, which manages message delivery.

The model consists of three main elements: publishers, subscribers, and the broker. A publisher sends data to the broker by publishing messages to a "topic." A subscriber receives these messages by subscribing to a topic. The broker receives messages from publishers and distributes them to subscribers.

MQTT supports different Quality of Service (QoS) levels for reliable message delivery and is ideal for low-resource systems. It is widely used in IoT, industrial automation, smart homes, and robotics.

### ⚡📨 QoS (Quality of Service)

- **QoS 0** The message is delivered once without acknowledgment; if lost, it is not resent.
- **QoS 1** Guarantees message delivery; the sender resends until acknowledged.
- **QoS 2** Ensures the message is delivered exactly once, with confirmation before deletion.

### ✅📊📡 Advantages of MQTT Communication

- 📦 Small messages → Low bandwidth and resource usage.
- 🔄 Versatile → Can send different types of data.
- 📡 Multiple topics → Devices can subscribe to several topics.
- 📬 Topic management → Messages are organized by topic for easy handling.
- ⚙️ Device control → Messages can contain multiple parameters for equipment control.

### 📤📡📥 Communication Structure Created

Due to its low processing requirements and adaptability, MQTT was chosen. The steps taken were:

1. **MQTT Clients Creation:** A ROS package mqtt for the communication node and an MQTT module for the robot handling connection, topics, subscription, publication, and JSON-formatted messages.

2. **Control Elements:** A Python script for robot actions and a ROS control package for both simulation and real robot control.

3. **Graphical Interface:** A teleoperation GUI package in ROS.

4. **Simulation:** Robot model deployment and expected behavior monitoring.

<div align="center">
    <img src="https://i.imgur.com/XTODCrV.png" alt="Estructura de la comunicación" width="800px">
</div>

### 🚀🌐🔧 Broker Creation and Configuration

We used [hivemq](https://www.hivemq.com/) to create a free broker (10 GB max traffic, up to 100 simultaneous sessions).

From the summary page, take the Cluster URL and Port values and insert them into both the ROS mqtt package and the robot's MQTT module.

<div align="center">
  <img src="https://imgur.com/oUNJSub.png" alt="Overview broker" width="800px">
</div>

>[!TIP]
>You can set default values in the modules to avoid entering them every time.

Then, in Access Management, create a username and password for security. For example:
Username: ```LegoEV301```
password: ```LegoEV301```

>[!NOTE]
>The robot naming format is "LegoEV3XX" where XX is the robot's ID.

<div align="center">
    <img src="https://imgur.com/3vD0VmO.png" alt="Credential Assignment" width="800px">
</div>

Next, in Web Client, log in with your credentials and subscribe to all topics (#) to monitor all traffic.

<div align="center">
  <img src="https://imgur.com/4hdQxiK.png" alt="Broker Traffic Review" width="800px">
</div>

### 💻🔄🤖 Uploading Files to the Robot

On the robot's terminal:

```sh
cd ~/tests/python/
mkdir MQTT
cd ~/tests/python/MQTT
```

Copy the files from ev3_mqtt_ros/Scripts/Robot:

```sh
cd ev3_mqtt_ros/Scripts/Robot
scp -r ./* robot@<Robot_IP_Address>:/home/robot/tests/python/MQTT/
```

## ▶️📜🖥️ Running the Programs

Below are example commands and basic tests.

### 📡🎮🤖 Robot Teleoperation

Test the robot teleoperation using the rqt plugin interface.

```sh
roslaunch ev3_launch_pkg ev3_teleop.launch
```

<div align="center">
  <a href="https://www.youtube.com/watch?v=hCdG2yltG18">
    <img src="https://img.youtube.com/vi/hCdG2yltG18/0.jpg" alt="Robot Teleoperation" width="600px">
  </a>
</div>

### 🧩🏙️🖥️ Application and rqt Plugin

Test the teleoperation via the GUI application and rqt plugin. Uncomment the following line in ```ev3_teleop.launch``` inside ```ev3_launch_pkg```:

```xml
<!-- include file="$(find gui)/launch/gui.launch"/-->
```

Recompile the package and run:

```sh
roslaunch ev3_launch_pkg ev3_teleop.launch
```

<div align="center">
  <a href="https://www.youtube.com/watch?v=J4IgCLKRch4" >
    <img src="https://img.youtube.com/vi/J4IgCLKRch4/0.jpg" alt="Application and rqt Plugin" width="600px">
  </a>
</div>

### 🎮📊🤖 Teleoperation and Simulation

Test teleoperation with the rqt plugin, RViz for reference frame visualization, and Gazebo for virtual environment simulation.

```sh
roslaunch ev3_launch_pkg ev3_teleop_simulate.launch
```

<div align="center">
  <a href="https://www.youtube.com/watch?v=NIEbXVXS-eo">
    <img src="https://img.youtube.com/vi/NIEbXVXS-eo/0.jpg" alt="Teleoperation and Simulation" width="600px">
  </a>
</div>

## 📚🔍 References
* [Lego Ev3 connection via Raspberry Pi](https://github.com/aws-samples/aws-builders-fair-projects/blob/master/reinvent-2019/lego-ev3-raspberry-pi-robot/README.MD) 
* [ROS from Lego Ev3](https://github.com/moriarty/ros-ev3)
* [ev3dev Python API](https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/latest/)
* [EV3 Motor Control with Python](https://www.youtube.com/watch?v=j0-ATIe6pqg) 
* [Using Lidar with Ev3](https://www.youtube.com/watch?v=JX0zeYa-faM) 
* [SSH from VS Code to Ev3](https://www.youtube.com/watch?v=uNSIOvqzAnY) 
* [Installing ROS Jade on Ev3](https://github.com/osmado/ev3dev_ros_distribution) 
* [ROS Blog about Lego Ev3](http://wiki.ros.org/Robots/EV3)
* [Ev3 and Arduino Connection](https://www.dexterindustries.com/howto/connecting-ev3-arduino/)
* [ROS Control of Ev3 with C++](https://www.youtube.com/watch?v=iRQqEKYDRI4)
* [Github - ROS Control of Ev3 with C++](https://github.com/srmanikandasriram/ev3-ros?tab=readme-ov-file)
* [ev3dev Python Library](https://github.com/ev3dev/ev3dev-lang-python)
* [ev3dev C++ Library](https://github.com/ddemidov/ev3dev-lang-cpp)
* [MQTT Communication with Ev3](https://www.youtube.com/watch?v=3bEbLf1KTK4 )
* [MQTT with python](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python)