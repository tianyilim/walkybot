#include<wiringSerial.h>
#include<wiringPi.h>
#include<iostream>
#include<iomanip>
using namespace std;


uint8_t PACKET_SIZE_RX 12
uint8_t PACKET_SIZE_TX 2

/* Short the RX and TX pins together on the Rpi.
Run the same logic as the recieve on the Arduino:
Take 0xFF as the start bit.

IDEA:
Start with a handshake (Fixed start and stop bit; defines length of packet, allows for more flexible data sizes)
*/

void init();

void 

void serialRx();	// Recieves a uint8_t array of PACKET_SIZE_RX
void serialTx();	// Transmits a uint8_t array of PACKET_SIZE_TX

int main(){
	init();


}

void init(){
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
}

