#include "Arduino.h"
#include "serial_manchester.h"
#include "decoder.h"
#include "CircularBuffer.h"


char ASCII = 0;
CircularBuffer buff(32);

void serial_manchester_init(){
	Serial3.begin(BAUD_RATE_MANCHESTER);
}

void serial_manchester_read(){
	int incomming_byte = -1;
	if (Serial3.available() > 0){
		incomming_byte = Serial3.read();
		//Serial.println(incomming_byte);
		if (incomming_byte != -1){
			buff.write(incomming_byte);
		}
	}
}

char get_ASCII() {
	int max_count = 32*32;
	int start_sequence[18] = {0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0};
	int sequence_count = 0;
	int temp[32];
	buff.read(temp);
	char ASCII = 0;
	int read = 0;
	int toShift = 0;
	for (int i = 0; i < max_count; i++){
		int lol = temp[read%32];
		read++;
		if (start_sequence[sequence_count] == lol){
			sequence_count++;
			
		}
		else{

			sequence_count = 0;
			read = toShift++; 
		}
		if (sequence_count == 18){
			
			
			for (int y = 0; y <=6;y++){
				int bitA = temp[read%32]; read++;
				int bitB = temp[read%32];
				read++;
				if (bitA == 0 && bitB == 1){
					int hey = exp(2,y);
					//Serial.print(hey);
					//Serial.print(" ");
					ASCII+= hey;
				}
			}
			
			//Serial.println("-");
			return ASCII;
		}
	}
	//Serial.println("-");
	return ASCII;
	
}

int exp(int base, int power){
	int r = 1;
	for (int i = 0; i <power; i++){
		r = r*base;
	}
	return r;
}
