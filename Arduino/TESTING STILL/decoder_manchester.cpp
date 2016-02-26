#include "Arduino.h"
#include "decoder_manchester.h"
#include "CircularBuffer.h"
#include <math.h>  

void decoder_manchester_init() {
 
}

char ASCII = 0;

char get_ASCII(CircularBuffer buff) {
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


