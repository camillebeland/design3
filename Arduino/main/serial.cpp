#include "Arduino.h"
#include "serial.h"
#include "decoder.h"

int incomming_byte = -1;

void serial_init(){
	Serial.begin(BAUD_RATE);
}

int serial_read(){
	incomming_byte = Serial.read();
	if (incomming_byte != -1){
		return incomming_byte;
	}
	else{
		return -1;
	}
}