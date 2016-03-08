#include "Arduino.h"
#include "manchester_receiver.h"
#include "decoder.h"
#include "CircularBuffer.h"
#include "RH_ASK.h"
#include <SPI.h> 

char ASCII = 0;
CircularBuffer buff(32);
RH_ASK manchester_receiver(MANCHESTER_BAUD_RATE);

void manchester_receiver_init(){
	manchester_receiver.init();
}

void manchester_receiver_read(){
	uint8_t buf[4];
    uint8_t buflen = sizeof(buf);
    if (driver.recv(buf, &buflen)) // Non-blocking
    {
        for (int y = 0; y<4 ;y++){
			incomming_byte = buf[y];
			for (int i= 0; i< 8; i++)
			{
				buff.write((incomming_byte & (1<<i)) >> i);
			}
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
	if !(checksum(temp)){
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
			ASCII = 0;
			for (int y = 0; y <7;y++){
				int bitA = temp[read%32]; read++;
				int bitB = temp[read%32];
				read++;
				if (bitA == 0 && bitB == 1){
					ASCII+= exp(2,y);
				}
			}
			
			//Serial.println("-");

			return ASCII;
		}
	}
	
	//Serial.println("-");
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
