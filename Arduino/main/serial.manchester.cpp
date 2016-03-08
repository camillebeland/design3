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
	char incomming_byte = -1;
	if(Serial3.available() > 4){
		for (int y = 0; y < 4; y++){
		incomming_byte = Serial3.read();
		if (incomming_byte != -1)
		{
			for (int i= 0; i< 8; i++)
			{
				buff.write((incomming_byte & (1<<i)) >> i);
			}
		}
		}
	}
}

char get_ASCII() {
	int max_count = 32*32;
	int start_sequence[18] = {0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0};
	int sequence_count = 0;
	int temp[32];
	buff.read(temp);
	Serial.println(" ");
	for (int i = 0; i< 32;i++){
		Serial.print(temp[i]);
	}
	
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
			int new_ASCII = 0;
			for (int y = 0; y <=6;y++){
				int bitA = temp[read%32]; read++;
				int bitB = temp[read%32];
				read++;
				if (bitA == 0 && bitB == 1){
					int hey = exp(2,y);
					//Serial.print(hey);
					//Serial.print(" ");
					new_ASCII+= hey;
				}
				else if(bitA == 1 && bitB == 0){
				}
				else{
					//manschester invalide
					return ASCII;
				}
			}
			ASCII = new_ASCII;
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
