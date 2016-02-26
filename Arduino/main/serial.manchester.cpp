#include "Arduino.h"
#include "serial_manchester.h"
#include "decoder.h"
#include "CircularBuffer.h"


char ASCII = 0;
CircularBuffer buff(32);

void serial_manchester_init(){
	Serial1.begin(BAUD_RATE_MANCHESTER);
}

bool serial_manchester_read(){
	int incomming_byte = -1;
	if (Serial1.available() > 0){
		incomming_byte = Serial1.read();
		if (incomming_byte != -1){
			buff.write(incomming_byte);
			return true;
		}
		return false;
	}
}

char get_ASCII() {
	int max_count = 40;
	int start_sequence[18] = {0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0};
	int sequence_count = 0;
	for (int i = 0; i < max_count; i++){
		if (*(start_sequence+sequence_count) == buff.read()){
			sequence_count++;
		}
		else{
			sequence_count = 0;
		}
		if (sequence_count == 18){
			char ASCII = 0;
			
			for (int y = 0; y <6;y++){
				int bitA = buff.read();
				int bitB = buff.read();
				if (bitA == 0 && bitB == 1){
					ASCII+= pow(2,y);
				}
			}
		}
	}
	return ASCII;
}