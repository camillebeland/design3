#include "Arduino.h"
#include "decoder.h"
#include "motors.h"
#include "TimerFour.h"

void decoder_init(){
	Timer4.initialize(TIMEOUT);
	Timer4.attachInterrupt(TIMEOUT_ISR);
	Timer4.stop();
}


State current_state = IDLE;
Function current_function;
int speed_param = DEFAULT_SPEED;
int param_count = 0;
char params[4] = {0};

// NO CIRCULAR BUFFER YET, RT PROCESSING

void reset_decoder(){
	Timer4.stop();
	Timer4.restart();
	current_state = IDLE;
}

bool decode_byte(char byte){
	
	bool byte_decoded = false;
	
	if(byte == START_CHAR){reset_decoder;};
	
	switch(current_state){
		
		case IDLE:
			if(byte == START_CHAR){
				current_state = FUNCTION;
				byte_decoded = true;
				param_count = 0;
				Serial.println("Start CHAR detected");
				Timer4.start();
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
				Serial.println("Function stop detected");
			}
			else if (byte == 'm' || byte == 'M'){
				current_function = MOVE;
				param_count = 4;
				Serial.println("Function move detected");
				if (byte == 'm'){speed_param = SLOW_SPEED;}
				else{ speed_param = DEFAULT_SPEED;}
				current_state = PARAMETERS;
			}
			else if (byte == 'r'){
				current_function = ROTATE;
				Serial.println("Function rotate detected");
				param_count = 2;
				current_state = PARAMETERS;
			}
			// cover errors
			else{
				byte_decoded = false;
				current_state = IDLE;
			}
		break;
		
		case PARAMETERS:
			byte_decoded = true;
			if (param_count >0){
				if (byte == END_CHAR){
					byte_decoded = false;
					current_state = IDLE;
				}
				params[4-param_count] = byte;
				param_count--;
			}
			//cover errors
			if (param_count <1){
				byte_decoded = true;
				current_state = END;
			}
			Serial.println("Parameter detected");
		break;
		
		case END:
			byte_decoded = true;
      
			if (byte == END_CHAR){
				parse_and_call();
				current_state =  IDLE;
				Serial.println("End CHAR detected");
			}
			//cover errors
			else{
				byte_decoded = false;
			}
		reset_decoder();
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
			if (params[2] =='l'){
				direction = LEFT;
			}
			else if(params[2] == 'r'){
				direction = RIGHT;
			}
			else{
				return false;
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

void TIMEOUT_ISR(){
	reset_decoder();
}
