#include<wiringSerial.h>
#include<wiringPi.h>
#include<iostream>
using namespace std;
// Include these to enable the hardware functionality

/*
	In this case we are testing one-way communications functionality between the Rpi and the Arduino.
	We simply increment a char from 0-255 and delay in 100ms intervals.
	Simple enough
*/

int main(){
	int fd;
	char x;

	// Opens up the default serial port on Pi 0. In this case it is "/ttyS0"
	// Don't forget to run the program as sudo.
	if( (fd = serialOpen("/dev/ttyS0", 9600)) < 0){
		cout << "Unable to open Serial Port" << endl;
		exit(1);
	}

	// Sets up wiringPi peripherals.
	if( wiringPiSetup()==-1 ){
		cout << "Unable to setup WiringPi" << endl;
		exit(2);
	}

	// Actual hard work here...
	for(x=0; x<256; x++){
		serialPutchar(fd, x);
		cout << "print " << int(x) << endl;
		delay(100);
	}

	// Don't forget to close the thing before exiting the prg.
	// Sounds ripe for making a class...
	serialClose(fd);
	return 0;

}