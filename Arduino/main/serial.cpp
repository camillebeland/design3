#include "Arduino.h"
#include "serial.h"
#include "decoder.h"

void serial_init(){
	Serial.begin(BAUD_RATE);
}

void serial_read(){
	int incomming_byte = -1;
	if (Serial.available() >0){
		incomming_byte = Serial.read();
		decode_byte(incomming_byte);
	}
}

void serial_write(int toWrite){
	Serial.write(toWrite);
}
