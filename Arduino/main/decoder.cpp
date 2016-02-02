#include "Arduino.h"
#include "decoder.h"

void decoder_init(){

}

bool decode_byte(char byte){
	
	if (byte == -1){
		return false;
	}
	else{
    switch(byte){
      case 'a':
        move_straight(LEFT, 10000, 500);
        break;
      case 'b':
        move_straight(FORWARD, 10000, 500);
        break;
      case 'c':
        rotate(LEFT, 1000);
        break;
      case 's':
        stop();
        break;
      default:
        break;
    }
		
		// DECODE AND CALL THE APPROPRIATE FUNCTION
		return true;
	}

}
