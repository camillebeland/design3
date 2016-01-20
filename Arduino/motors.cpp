#include "Arduino.h"
#include "motor.h"

void motor_init(){
	attachInterrupt(digitalPinToInterrupt(INT_ENCODER_A_CH1), count_tick_A, RISING);
	attachInterrupt(digitalPinToInterrupt(INT_ENCODER_B_CH1), count_tick_B, RISING);
	attachInterrupt(digitalPinToInterrupt(INT_ENCODER_C_CH1), count_tick_C, RISING);
	attachInterrupt(digitalPinToInterrupt(INT_ENCODER_D_CH1), count_tick_D, RISING);	
	
	pinMode(OUT_MOTOR_1, OUTPUT);
	pinMode(OUT_MOTOR_2, OUTPUT);
	pinMode(OUT_MOTOR_3, OUTPUT);
	pinMode(OUT_MOTOR_4, OUTPUT);
	
	analogWrite(OUT_MOTOR_1, ZERO_SPEED);	
	analogWrite(OUT_MOTOR_2, ZERO_SPEED);	
	analogWrite(OUT_MOTOR_3, ZERO_SPEED);	
	analogWrite(OUT_MOTOR_4, ZERO_SPEED);	
}

int tick_remaining_A = 0;
int tick_remaining_B = 0;
int tick_remaining_C = 0;
int tick_remaining_D = 0;

void move(int &direction, int & tick){
	
	//set motors of interest + read initial state
	if (direction == FORWARD || direction == BACKWARD){
		tick_remaining_A = tick;
		tick_remaining_C = tick;
		int OUT_MOTOR_X = OUT_MOTOR_A;
		int OUT_MOTOR_Y = OUT_MOTOR_C;
		if (direction == FORWARD){
			int polarity = 1;
		}
		else{
			int polarity = -1;
		}
	}
	else if (direction == LEFT || direction == RIGHT){
		tick_remaining_B = tick;
		tick_remaining_D = tick;
		int OUT_MOTOR_X = OUT_MOTOR_B;
		int OUT_MOTOR_Y = OUT_MOTOR_D;		
		if (direction == LEFT){
			int polarity = 1;
		}
		else{
			int polarity = -1;
		}
	}
	
	int PID_X = 0;
	int PID_Y = 0;
	
	unsigned long last_millis = 0;
	int wanted_speed = DEFAULT_SPEED;
	int last_tick_remaining_X = tick;
	int last_tick_remaining_Y = tick;
	int tick_remaining_X = tick;
	int tick_remaining_Y = tick;
	
	// -------------------------------------------------------------------------//
	//PID STUFF HERE 
	while (tick_remaining_X > 0 || tick_remaining_Y > 0){
		if (millis() - last_millis >= DT)
		{
			if (direction == LEFT || direction == RIGHT){
				tick_remaining_X = tick_remaining_A;
				tick_remaining_Y = tick_remaining_C;
			}
			else if (direction == FORWARD || direction == BACKWARD){
				tick_remaining_X = tick_remaining_B;
				tick_remaining_Y = tick_remaining_D;
			}
			
			if (tick_remaining_X < CRITICAL_TICK || tick_remaining_Y < CRITICAL_TICK){
				wanted_speed = DEFAULT_SPEED / 4;
			}
		
			last_millis = millis();
			int error_X = wanted_speed -  (last_tick_remaining_X - tick_remaining_X);
			int error_Y = wanted_speed -  (last_tick_remaining_Y - tick_remaining_Y);
			PID_X +=(error_X * KI);
			PID_Y +=(error_Y * KI);			

			analogWrite(OUT_MOTOR_X, ZERO_SPEED + (polarity*PID_X));
			analogWrite(OUT_MOTOR_Y, ZERO_SPEED + (polarity*PID_Y));
			
			last_tick_remaining_X = tick_remaining_X;
			last_tick_remaining_Y = tick_remaining_Y;
		}
		// END OF PID STUFF
		// --------------------------------------------------------------------------------------//
	}
	//turn off motors
	analogWrite(OUT_MOTOR_X, ZERO_SPEED);
	analogWrite(OUT_MOTOR_Y, ZERO_SPEED);
	
	//RESETS TICKS
	tick_remaining_A = 0;
	tick_remaining_B = 0;
	tick_remaining_C = 0;
	tick_remaining_D = 0;
}

void count_tick_A(){
	tick_remaining_A--;
}
void count_tick_B(){
	tick_remaining_B--;
}
void count_tick_C(){
	tick_remaining_C--;
}
void count_tick_D(){
	tick_remaining_D--;
}
