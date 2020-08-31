# walkybot
Programs and drivers for a Hexapod

# Test phase
## Serial communications:
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

## Inverse Kinematics
Servo angle calculations based on the desired end point of a foot.
This requires a degree of maths.

## Simulation in ROS
Self explanatory. Attempt to simulate the robot's motion fully (or partially?) in ROS here before deploying to actual hardware to minimise debugging time.

## Add-Ons ?
Future work. The child in me wants to add a laser turret or something "*useful*" of that sort.