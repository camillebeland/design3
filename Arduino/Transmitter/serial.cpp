#include "Arduino.h"
#include "serial.h"

void serial_init(){
	Serial1.begin(BAUD_RATE);
}

int serial_send_manchester(int * ptr){
	int * local = ptr;
	for (int i = 0; i<32;i++){
		Serial1.write(*local);
		local++;
	}
}