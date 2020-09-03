# walkybot
Programs and drivers for a Hexapod

## Inverse Kinematics
- Leg IK is implemented here based on material from https://oscarliang.com/inverse-kinematics-implementation-hexapod-robots/. A rough version currently exists within the `walkybot_testbench` notebook.
- Body IK is being understood at the moment.

For now, a "Wave" gait shall be implemented - the simplest kind of gait whereby legs move one by one.
Next, a "Ripple" gait would be implemented, and a "Tripod" gait would be implemented last.

#### Future Extensions
- Negative feedback with accelerometer data
- Dynamic gait selection based on input speed

## GCS to Robot communications
- Create a GUI for robot data:
1. Battery Level, current consumption
2. Controller inputs
3. Accelerometer artificial horizon
4. Selected gait
The input for the direction of the robot will be controlled by a USB Xbox-360 controller, via the Python `inputs` module.

# Content below is depreceated
A previous iteration of this project intended to use a Raspberry Pi for computation and a Arduino for controlling servos. However, a pair of PCA9685 servo controllers have been employed instead, which removes the requirement for an Arduino.

## Test phase
### Serial communications:
The servo angle calculations are done on the Pi and sent to the Arduino to be done.
Communication can be bidirectional; for instance if there are sensors connected to the arduino that requires reading.
_TODO_
- Come up with a class (RPi side) to easily handle the communication between the two.
- The class should have the following:
	- Constructor initializes WiringPi and starts the serial port
	- Destructor frees up the serial port
	- Handshake (initializes serial communication)
	- Serial RX
	- Serial TX
- Member variables are the **input** and **output** buffers

- Arduino side communications can be handled 'easily' with its own driver software. Functions in the sketch are ok, no need for an additional class.

### Simulation in ROS
Self explanatory. Attempt to simulate the robot's motion fully (or partially?) in ROS here before deploying to actual hardware to minimise debugging time.

### Add-Ons ?
Future work. The child in me wants to add a laser turret or something "*useful*" of that sort.