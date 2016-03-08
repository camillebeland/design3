#include "Arduino.h"
#include "manchester_transmitter.h"
#include "RH_ASK.h"
#include <SPI.h> 

RH_ASK manchester_transmitter(BAUD_RATE);

void manchester_transmitter_init(){
	transmitter.init();
}

int manchester_transmitter_send(int * ptr){
	int * local = ptr;
	char chars[4] = {0,0,0,0};
	for (int i = 0; i<32;i++){
		chars[i/8] |= *local << (i%8);
		local++;
	}
	
	manchester_transmitter.send(chars, 4);
}
