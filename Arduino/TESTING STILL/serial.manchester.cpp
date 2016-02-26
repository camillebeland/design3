#include "Arduino.h"
#include "serial_manchester.h"
#include "decoder.h"
#include "CircularBuffer.h"

int incomming_byte = -1;
CircularBuffer buff(32);

void serial_manchester_init(){
	Serial1.begin(BAUD_RATE);
}

bool serial_manchester_read(){
	incomming_byte = Serial.read();
	if (incomming_byte != -1){
		buff.write(incomming_byte);
		return true;
	}
	return false;
}

CircularBuffer get_manchester(){
	CircularBuffer temp(buff);
	return temp;
}
