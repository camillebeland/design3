#include "Arduino.h"
#include "serial.h"

void serial_init(){
	Serial1.begin(BAUD_RATE);
}

int serial_send_manchester(int * ptr){
	char * charptr = (char*)ptr;
	Serial1.write(charptr, 32);
}