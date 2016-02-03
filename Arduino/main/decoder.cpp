#include "Arduino.h"
#include "decoder.h"
#include "motors.h"

void decoder_init(){

}


State current_state = IDLE;
Function current_function;
int speed_param = DEFAULT_SPEED;
int param_count = 0;
char params[4] = {0};


// STILL MISSING A TIMEOUT FEATURE

bool decode_byte(char byte){
	
	bool byte_decoded = false;
	
	switch(current_state){
		
		case IDLE:
			if(byte == START_CHAR){
				current_state = FUNCTION;
				byte_decoded = true;
			}
			else{
				byte_decoded = false;
			}
		break;
		
		case FUNCTION:
		    byte_decoded = true;
			if (byte == 's'){
				current_function = STOP;
				current_state = END;
			}
			else if (byte == 'm' || byte == 'M'){
				current_function = MOVE;
				param_count = 4;
				if (byte == 'm'){speed_param = SLOW_SPEED;}
				else{ speed_param = DEFAULT_SPEED;}
				current_state = PARAMETERS;
			}
			else if (byte == 'r'){
				current_function = ROTATE;
				param_count = 2;
				current_state = PARAMETERS;
			}
			else{
				byte_decoded = false;
				current_state = IDLE;
			}
		break;
		
		case PARAMETERS:
			byte_decoded = true;
			if (param_count >0){
				params[4-param_count] = byte;
				param_count--;
			}
			else{
				byte_decoded = false;
				current_state = END;
			}
		break;
		
		case END:
			byte_decoded = true;
			if (byte == END_CHAR){
				parse_and_call();
				current_state =  IDLE;
				param_count = 0;
			}
			else{
				byte_decoded = false;
			}
		break;
		
		
		default:
			current_state = IDLE;
			byte_decoded = false;
		break;
	
	}
	return byte_decoded;
}

bool parse_and_call(){
	int angle, x, y;
	switch(current_function){
		case STOP:
			stop();
		break;
		
		case ROTATE:
			Direction direction;
			if (params[2] =='L'){
				direction = LEFT;
			}
			else if(params[2] == 'R'){
				direction = RIGHT;
			}
			angle= int(params[3]);
			rotate(direction, angle);	
		break;
		
		case MOVE:
			x = int((params[0] << 8) + params[1]);
			y = int((params[2] << 8) + params[3]);
			move(x, y, speed_param);
		break;
		
		default:
			return false;
		break;
		}
	return true;
}
