#include "Arduino.h"
#include "motor.h"

void motor_init(){
	pinMode(IN_ENCODER_1_CH1, INPUT);
	pinMode(IN_ENCODER_1_CH2, INPUT);
	pinMode(IN_ENCODER_2_CH1, INPUT);
	pinMode(IN_ENCODER_2_CH2, INPUT);
	pinMode(IN_ENCODER_3_CH1, INPUT);
	pinMode(IN_ENCODER_3_CH2, INPUT);
	pinMode(IN_ENCODER_4_CH1, INPUT);
	pinMode(IN_ENCODER_4_CH2, INPUT);
	
	pinMode(OUT_MOTOR_1, OUTPUT);
	pinMode(OUT_MOTOR_2, OUTPUT);
	pinMode(OUT_MOTOR_3, OUTPUT);
	pinMode(OUT_MOTOR_4, OUTPUT);
	
	analogWrite(OUT_MOTOR_1, ZERO_SPEED);	
	analogWrite(OUT_MOTOR_2, ZERO_SPEED);	
	analogWrite(OUT_MOTOR_3, ZERO_SPEED);	
	analogWrite(OUT_MOTOR_4, ZERO_SPEED);	
}

void move(int &direction, int & tick){
	
	//tick remaining for each motor
	int tick_left_X = tick;
	int tick_left_Y = tick;
	
	//set motors of interest + initial state + default speed
	if (direction == FORWARD || direction == LEFT){
		int OUT_MOTOR_X = OUT_MOTOR_1;
		int OUT_MOTOR_Y = OUT_MOTOR_3;
		
		int motor_X_ch_one = digitalRead(IN_ENCODER_1_CH1);
		int motor_X_ch_two = digitalRead(IN_ENCODER_1_CH2);
		int motor_Y_ch_one = digitalRead(IN_ENCODER_3_CH1);
		int motor_Y_ch_two = digitalRead(IN_ENCODER_3_CH2);	
		
		int default_speed = ZERO_SPEED + DEFAULT_SPEED;
	}
	if (direction == BACKWARD || direction == RIGHT){
		int OUT_MOTOR_X = OUT_MOTOR_2;
		int OUT_MOTOR_Y = OUT_MOTOR_4;		
		
		int motor_X_ch_one = digitalRead(IN_ENCODER_2_CH1);
		int motor_X_ch_two = digitalRead(IN_ENCODER_2_CH2);
		int motor_Y_ch_one = digitalRead(IN_ENCODER_4_CH1);
		int motor_Y_ch_two = digitalRead(IN_ENCODER_4_CH2);

		int start_speed = ZERO_SPEED - DEFAULT_SPEED;
	}
	
	int PID_X = 0;
	int PID_Y = 0;
	
	while (tick_left_X > 0 || tick_left_Y > 0){
		analogWrite(OUT_MOTOR_X, start_speed + PID_X);
		analogWrite(OUT_MOTOR_Y, start_speed + PID_Y);
		
		// THE FOLLOWING TO PUT IN GLOBAL VARIABLE/INTERUPT
		if (digital(IN_ENCODER_1_CH1) != wheel_one_ch_one){
			tick_left_X--;
			motor_X_ch_one = digital(IN_ENCODER_1_CH1);
		}
		if (digitalRead(IN_ENCODER_1_CH2) != wheel_one_ch_two){
			tick_left_X--;
			motor_X_ch_two = digitalRead(IN_ENCODER_1_CH2);
		}
		if (digital(IN_ENCODER_3_CH1) != wheel_three_ch_one){
			tick_left_Y--;
			motor_Y_ch_one = digital(IN_ENCODER_3_CH1) ;
		}
		if (digitalRead(IN_ENCODER_3_CH2) != wheel_three_ch_two){
			tick_left_Y--;
			motor_Y_ch_two = digitalRead(IN_ENCODER_3_CH2);
		}
		// --------------------------------------------------------------------------------------//
		// DO THE PID STUFF HERE 
		// Regulator FOR tick_left (distance left)
		// Regulator FOR (motor 1 vs motor 3, same speed or position)
		// --------------------------------------------------------------------------------------//	
	}
	//turn off motors
	analogWrite(OUT_MOTOR_X, ZERO_SPEED);
	analogWrite(OUT_MOTOR_Y, ZERO_SPEED);
}