# Enabling Safe and Stable Drone Delivery

Author: Henry Buron

View the portfolio post: [https://henryburon.github.io/drone-delivery/](https://henryburon.github.io/drone-delivery/)

### Contents
1. [System Description](#system-description)
2. [System Setup and Notes](#system-setup-and-notes)
3. [Drone Manuel](#drone-manual)

## System Description

This repository is for a drone-based delivery system that delivers a package via tether. The package--in the form of a small mobile robot--stabilizes itself during descent, and has the ability to release itself from the tether and drive along the ground towards its destination.

![full_system](https://github.com/user-attachments/assets/4b4239d5-7273-40f9-a8d8-f7f85fa497cb)

The system consists of three main parts:

1. Drone and Winch
- Heavy payload drone, designed and built by [Marno Nel](https://marnonel6.github.io/projects/0-autonomous-px4-drone).
- Custom-built winch system.
- The drone receives winch commands via a LoRa module connected to an Arduino Nano. The Arduino Nano, connected via USB to the drone's on-board Raspberry Pi, forwards those messages over serial. A script running on the Raspberry Pi continuously reads the serial buffer and converts those commands into a PWM signal which is sent to the winch's servo motor.
2. Mobile Package Robot
- Mechanical and electrical system built from scratch. Communicates via LoRa.
- Capable of safely storing a small quantity of medical or emergency supplies.
- Stabilizes itself during descent using its lateral propellers.
- Releases itself from the winch's tether once its on the ground.
- Capable of driving over smooth terrain closer to its target destination.
3. Base Station
- Consists of a Lora module and Arduino nano.
- A script on the base station computer sends commands over serial to the Nano which then sends them over LoRa.

## System Setup and Notes

## SSH

On NUMSR WiFi

Drone/Winch (RPi 4): `ssh osprey@osprey`  
PW: osprey

Mobile Robot (RPi 5): `ssh henry@droid`  
PW: robotics!

With Ethernet cable:

Drone/Winch (RPi 4): `ssh osprey@10.42.0.2`  
PW: osprey

Mobile Robot (RPi 5): `ssh henry@10.42.0.3`
PW: robotics!

Note: Ethernet ports have been given the above static IPs.


## Drone Manual

Designed for use with Marno Nel's [drone_control package](https://github.com/Marnonel6/ROS2_offboard_drone_control/tree/main) and [custom 15" PX4-Based Quadcopter](https://marnonel6.github.io/projects/0-autonomous-px4-drone).

### Contents

1. [Manual Flight](#manual-flight)
2. [Autonomous Flight](#autonomous-flight)
3. [Other](#other)  
   * [Important Information](#important-information)
   * [Pre-Flight Checklist](#pre-flight-checklist)
   * [Post-Flight Checklist](#post-flight-checklist)
   * [QGroundControl](#qgroundcontrol)
   * [Simulation](#simulation)


### Manual Flight

**Before flight, follow the [Pre-Flight Checklist](#pre-flight-checklist)**

The drone can be flown manually with the RadioMaster TX16 Controller (RC). This does not require the Raspberry Pi to be powered.


1. Ensure correct drone configuration, including RC's button and stick mapping.  
   * See [QGroundControl](#qgroundcontrol) for more information.
2. Power the Pixhawk and motors with a 6s LiPo battery.  
   * ESCs should beep. If not, check connections.
3. ARM the drone by moving the RC sticks to the ARM configuration (L-->BR; R-->BL).  
   * ESCs should beep again. If not, connect to QGroundControl and see error.
   * Once armed, the drone is ready for flight.
4. Slowly increase the throttle to lift off smoothly.
5. Once landed, DISARM the drone (L-->BL; R-->BR).


### Autonomous Flight

**Before flight, follow the [Pre-Flight Checklist](#pre-flight-checklist)**

The drone can be controlled autonomously via the C++ [drone_control](https://github.com/Marnonel6/ROS2_offboard_drone_control/blob/main/drone_control/src/drone_control.cpp) state machine using ROS2 and PX4. This code manages the drone's flight along a planned path by handling waypoints and different flight modes.

An example can be seen [here](https://github.com/Marnonel6/ROS2_offboard_drone_control/blob/main/drone_control/src/path_planning.cpp).

The Raspberry Pi must be powered and connected to the Pixhawk. 

On NUMSR WiFi, connect with: `ssh osprey@192.168.18.150`  
Password: `osprey`

Drone states include: `PREFLIGHT`, `IDLE`, `OFFBOARD`, `MISSION`, `LAND`, `RTL`, `FAIL`, `LIMBO`, and `ERROR`.

Methods include:  
`publish_offboard_control_mode()`: Publishes the off-board control mode.  
`publish_trajectory_setpoint()`: Publishes a trajectory setpoint for the drone.  
`arm()`: Arms the drone.  
`disarm()`: Disarms the drone.  
`takeoff()`: Sends a takeoff command to the drone.  
`land()`: Sends a land command to the drone.  
`RTL()`: Sends a return-to-launch command to the drone.  
`publish_vehicle_command`: Publishes various vehicle commands.  


### Other

#### Important Information

* To fly the drone, you must first pass [The Recreational UAS Safety Test (TRUST)](https://www.faa.gov/uas/recreational_flyers/knowledge_test_updates).
* To fly the drone on Northwestern property, you must follow the University's [official guidance](https://www.faa.gov/uas/recreational_flyers/knowledge_test_updates), including flying in the designated UAS zones.

#### Pre-Flight Checklist

1. Mission Planning  
   * Use the B4UFLY app to verify your flight location.  
   * Ensure appropriate weather conditions.
2. Hardware Check  
   * Ensure batteries are charged; check for damage, swelling.
   * With batteries disconnected, check propellers are secured.
   * Check frame and body for any damage or cracks.
3. Connect Pixhawk to QGroundControl.  
   * Check for errors on main screen.
   * Ensure GPS can find satellites.
   * Ensure failsafe settings are configured correctly.
4. Takeoff  
   * Ensure the takeoff area is clear and flat.

Launch the node to begin autonomous flight. For safety purposes, control can be switched back to manual at any time via flipping the RC's MANUAL control stick. In emergencies, flip the KILL switch to immediately cut power to the drone. This should be used with caution, as the drone will likely take damage.

#### Post-Flight Checklist

1. DISARM the drone (L-->BL; R-->BR).
2. Power down.  
   * Disconnect the batteries after safely shutting down the Raspberry Pi.
3. Inspect the drone hardware for damage.  
   * Pay particular attention to the batteries. Check for swelling.
   * Check propellers for cracks.
   * Ensure all screws and nuts are tight and secure.

#### QGroundControl

QGroundControl is an open-source ground control station software designed for use with drones and other unmanned vehicles. It provides an interface for flight planning, monitoring, and management.

View the QGroundControl User Guide [here](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/).

For our purposes, we can use QGroundControl to:  
   * Manually ARM the drone.
   * Check for error messages.
   * Monitor the drone during flight.
   * Change flight configurations.
   * Tune the flight controller (i.e. PID values)
   * Remap the Radio Controller.

The drone can be connected to the ground station either manually (i.e. cable between Pixhawk and laptop) or wirelessly (i.e. with a telemetry unit).

![sample_qgroundcontrol](https://github.com/henryburon/stable-drone-delivery/assets/141075086/f731c737-79ba-47ad-a6bc-9fb505aa8965)

Example QGroundControl interface before flight.

#### Simulation

View simulation instructions [here](https://github.com/Marnonel6/ROS2_offboard_drone_control/tree/main?tab=readme-ov-file#sitl-simulation).

