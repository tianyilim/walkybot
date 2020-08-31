#include<wiringSerial.h>
#include<wiringPi.h>
#include<iostream>
#include<iomanip>
using namespace std;
// Include these to enable the hardware functionality

/*
	In this case we are testing one-way communications functionality between the Rpi and the Arduino.
	We simply increment a char from 0-255 and delay in 100ms intervals.
	Simple enough
*/

int main(){
	int fd;
	uint8_t servoData[12];

	// Opens up the default serial port on Pi 0. In this case it is "/ttyS0"
	// Don't forget to run the program as sudo.
	if( (fd = serialOpen("/dev/ttyS0", 9600)) < 0){
		cout << "Unable to open Serial Port, have you enabled sudo?" << endl;
		exit(1);
	}

	// Sets up wiringPi peripherals.
	if( wiringPiSetup()==-1 ){
		cout << "Unable to setup WiringPi" << endl;
		exit(2);
	}

	// Actual hard work here. We wish to send data packets over to the Arduino.
	// Let's just say that data is a 32-bit integer.
	// Send 0xFF as start bit. Then have two bits that are behind.
	// Software control that data to be transmitted cannot take the value 0xFF...
	// Ensure that start bit is always at that value? Should not be an issue if we
	// use Unsigned numbers always
	// Can scale servo positions to be 0-180(uint8_t); no issues here.
	// Sensor data though?
	for(int i=0; i<10; i++){

		// Update array values
		for(int j=0; j<12; j++){
			servoData[j] = (int)j*i;
		}

		// Send start bit;
		serialPutchar(fd, 0xFF);

		//send array of values;
		cout << "Sending: ";
		for(int j=0; j<12; j++){
			cout << hex << (int)servoData[j] << " ";
			serialPutchar(fd, servoData[j]);
			// Put a delay here to ensure that data is transmitted properly and no bits are skipped.
			delay(1);
		}
		cout << endl;

		serialFlush(fd);

		delay(100);

	}

	// Don't forget to close the thing before exiting the prg.
	// Sounds ripe for making a class...
	serialClose(fd);
	return 0;

}