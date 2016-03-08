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
	if(Serial3.available() >=4){
		for (int y = 0; y<4 ;y++){
			incomming_byte = Serial3.read();
			for (int i= 0; i< 8; i++)
			{
				buff.write((incomming_byte & (1<<i)) >> i);
			}
		}
		while (Serial3.available()){
			Serial3.read();
		}
	}
}

char get_ASCII() {

	int max_count = 32*32;
	// Manchester sequence before the data
	int start_sequence[18] = {0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0};
	int sequence_count = 0;
	int temp[32];
	buff.read(temp);
	if (!checksum(temp)){
		return ASCII;
	}
	/*
	Serial.println(" ");
	for (int i = 0; i< 32;i++){
		Serial.print(temp[i]);
	}
	*/
	int read = 0;
	int toShift = 0;
	while (toShift < 32){
		int current_bit = temp[read%32];
		read++;
		if (start_sequence[sequence_count] == current_bit){
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
					new_ASCII+= exp(2,y);
				}
			}
			ASCII = new_ASCII;
		}
	}
	
	return ASCII;
}

bool checksum(int *ptr){
	int sum = 0;
	for (int i = 0; i < 32; i++){
		sum+= *ptr;
		ptr++;
	}
	if (sum == 16){
		return true;
	}
	return false;
}

int exp(int base, int power){
	int r = 1;
	for (int i = 0; i <power; i++){
		r = r*base;
	}
	return r;
}
