#include "Arduino.h"
#include "manchester_transmitter.h"
#include "RH_ASK.h"
#include <SPI.h> 

RH_ASK manchester_transmitter(BAUD_RATE, 0, TX_PIN, 0 , false);

void manchester_transmitter_init(){
	manchester_transmitter.init();
}

int manchester_transmitter_send(int * ptr){
	int * local = ptr;
	uint8_t chars[4] = {0,0,0,0};
	for (int i = 0; i<32;i++){
		chars[i/8] |= *local << (i%8);
		local++;
	}
	manchester_transmitter.send(chars, 4);
	manchester_transmitter.waitPacketSent();
}
