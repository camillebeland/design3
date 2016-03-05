#include "Arduino.h"
#include "serial.h"

void serial_init(){
	Serial1.begin(BAUD_RATE);
}

int serial_send_manchester(int * ptr){
	int * local = ptr;
	char chars[4] = {0,0,0,0};
	for (int i = 0; i<32;i++){
		chars[i/8] |= *local << (i%8);
		local++;
	}
	Serial1.write(chars, 4);
	
}
