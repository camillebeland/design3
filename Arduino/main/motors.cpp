#include "Arduino.h"
#include "motors.h"

void motor_init(){
	pinMode(INT_ENCODER_A_CH1, INPUT);
	//pinMode(INT_ENCODER_B_CH1, INPUT);
	//pinMode(INT_ENCODER_C_CH1, INPUT);
	//pinMode(INT_ENCODER_D_CH1, INPUT);

	attachInterrupt(digitalPinToInterrupt(INT_ENCODER_A_CH1), count_tick_A, RISING);
	//attachInterrupt(digitalPinToInterrupt(INT_ENCODER_B_CH1), count_tick_B, RISING);
	//attachInterrupt(digitalPinToInterrupt(INT_ENCODER_C_CH1), count_tick_C, RISING);
	//attachInterrupt(digitalPinToInterrupt(INT_ENCODER_D_CH1), count_tick_D, RISING);	
	
	pinMode(OUT_MOTOR_A, OUTPUT);
	//pinMode(OUT_MOTOR_B, OUTPUT);
	//pinMode(OUT_MOTOR_C, OUTPUT);
	//pinMode(OUT_MOTOR_D, OUTPUT);
	
	pinMode(PIN_ONE_MOTOR_A, OUTPUT);
	//pinMode(PIN_ONE_MOTOR_B, OUTPUT);
	//pinMode(PIN_ONE_MOTOR_C, OUTPUT);
	//pinMode(PIN_ONE_MOTOR_D, OUTPUT);
	
	pinMode(PIN_TWO_MOTOR_A, OUTPUT);
	//pinMode(PIN_TWO_MOTOR_B, OUTPUT);
	//pinMode(PIN_TWO_MOTOR_C, OUTPUT);
	//pinMode(PIN_TWO_MOTOR_D, OUTPUT);

	digitalWrite(PIN_ONE_MOTOR_A, LOW);
	//digitalWrite(POLARITY_A_MOTOR_B, LOW);
	//digitalWrite(POLARITY_A_MOTOR_C, LOW);
	//digitalWrite(POLARITY_A_MOTOR_D, LOW);
	
	digitalWrite(PIN_TWO_MOTOR_A, LOW);
	//digitalWrite(POLARITY_B_MOTOR_B, LOW);
	//digitalWrite(POLARITY_B_MOTOR_C, LOW);
	//digitalWrite(POLARITY_B_MOTOR_D, LOW);
	
	analogWrite(OUT_MOTOR_A, ZERO_SPEED);	
	//analogWrite(OUT_MOTOR_B, ZERO_SPEED);	
	//analogWrite(OUT_MOTOR_C, ZERO_SPEED);	
	//analogWrite(OUT_MOTOR_D, ZERO_SPEED);	
	
}

//-------------------------------------------------------------------------------
// GLOBAL VARIABLES
int tick_remaining_A = 0;
int tick_remaining_B = 0;
int tick_remaining_C = 0;
int tick_remaining_D = 0;
int last_tick_remaining_A = 0;
int last_tick_remaining_B = 0;
int last_tick_remaining_C = 0;
int last_tick_remaining_D = 0;

unsigned long last_millis = 0;

bool polarity_A;
bool polarity_B;
bool polarity_C;
bool polarity_D;

double PID_A = 0;
double PID_B = 0;
double PID_C = 0;
double PID_D = 0;

double wanted_speed_A = 0;
double actual_speed_A = 0;
double wanted_speed_B = 0;
double actual_speed_B = 0;
double wanted_speed_C = 0;
double actual_speed_C = 0;
double wanted_speed_D = 0;
double actual_speed_D = 0;

bool straight_X = false;
bool straight_Y = false;

bool GO = false;

//-------------------------------------------------------------------------------

//move individual wheel
void move_wheel(int wheel, int wheel_tick, bool polarity,  int wheel_speed){
	
	if (wheel == OUT_MOTOR_A){
		tick_remaining_A += wheel_tick;
		last_tick_remaining_A += wheel_tick;
		wanted_speed_A= wheel_speed;
		polarity_A = polarity;
		if (polarity_A){
			digitalWrite(PIN_ONE_MOTOR_A, HIGH);
			digitalWrite(PIN_TWO_MOTOR_A, LOW);
		}
		else{
			digitalWrite(PIN_ONE_MOTOR_A, LOW);
			digitalWrite(PIN_TWO_MOTOR_A,  HIGH);		
		}
		straight_X = false;
	}
	else if(wheel == OUT_MOTOR_B){
		tick_remaining_B += wheel_tick;
		wanted_speed_B= wheel_speed;
		polarity_B = polarity;
		if (polarity_B){
			digitalWrite(PIN_ONE_MOTOR_B, HIGH);
			digitalWrite(PIN_TWO_MOTOR_B, LOW);
		}
		else{
			digitalWrite(PIN_ONE_MOTOR_B, LOW);
			digitalWrite(PIN_TWO_MOTOR_B,  HIGH);		
		}
		straight_Y = false;
	}
	else if (wheel == OUT_MOTOR_C){
		tick_remaining_C += wheel_tick;
		wanted_speed_C= wheel_speed;
		polarity_C = polarity;
		if (polarity_C){
			digitalWrite(PIN_ONE_MOTOR_C, HIGH);
			digitalWrite(PIN_TWO_MOTOR_C, LOW);
		}
		else{
			digitalWrite(PIN_ONE_MOTOR_C, LOW);
			digitalWrite(PIN_TWO_MOTOR_C,  HIGH);		
		}
		straight_X = false;
	}
	else if(wheel == OUT_MOTOR_D){
		tick_remaining_D += wheel_tick;
		wanted_speed_D= wheel_speed;
		polarity_D = polarity;
		if (polarity_D){
			digitalWrite(PIN_ONE_MOTOR_D, HIGH);
			digitalWrite(PIN_TWO_MOTOR_D, LOW);
		}
		else{
			digitalWrite(PIN_ONE_MOTOR_D, LOW);
			digitalWrite(PIN_TWO_MOTOR_D,  HIGH);		
		}
		straight_Y = false;
	}
	GO = true;

}
// move forward, backward, left or right
void move_straight(int direction, int tick, int speed){
	
	//set movement parameters, choose the appropriate motors to use

	if (direction == LEFT){
		move_wheel(OUT_MOTOR_A, tick, false, speed);
		move_wheel(OUT_MOTOR_C, tick, true, speed);
		straight_X = true;
	}
	else if (direction == RIGHT){
		move_wheel(OUT_MOTOR_A, tick, true, speed);
		move_wheel(OUT_MOTOR_C, tick, false, speed);
		straight_X = true;
	}
	else if (direction == FORWARD){
		move_wheel(OUT_MOTOR_B, tick, false, speed);
		move_wheel(OUT_MOTOR_D, tick, true, speed);
		straight_Y = true;
	}
	else	if (direction == BACKWARD){
		move_wheel(OUT_MOTOR_B, tick, true, speed);
		move_wheel(OUT_MOTOR_D, tick, false, speed);
		straight_Y = true;
	}
	
}

void move(float angle, int tick, int speed){
	//to implement using 2 move_straight calls
}

// PID for every wheel 
// TO DO -> modify regulator
// right now, comparing speeds of two wheel to go straight, apply feedback with the difference
// compute estimated position and compare to wanted final position
// will need testing on the physical robot
void PID_motors(){
	if (GO){
			unsigned long dt = millis() - last_millis;
			if (dt >= DT){
				
				//speed is tick/dt
				actual_speed_A = (last_tick_remaining_A - tick_remaining_A)/dt;
				actual_speed_B = (last_tick_remaining_B - tick_remaining_B)/dt;
				actual_speed_C = (last_tick_remaining_C - tick_remaining_C)/dt;
				actual_speed_D = (last_tick_remaining_D - tick_remaining_D)/dt;
				
				// Error = difference to wanted speed
				int error_A = wanted_speed_A - actual_speed_A;
				int error_B = wanted_speed_B - actual_speed_B;
				int error_C = wanted_speed_C - actual_speed_C;
				int error_D = wanted_speed_D - actual_speed_D;				
				
				int delta_motors_X = 0;
				if (straight_X){
					delta_motors_X =  actual_speed_A  - actual_speed_C ;
				}
				int delta_motors_Y = 0;
				if (straight_Y){
					delta_motors_Y =actual_speed_B - actual_speed_D;
				}
				
				PID_A +=(error_A * KI) - (delta_motors_X*KS);
				PID_B +=(error_B * KI) + (delta_motors_Y*KS);
				PID_C +=(error_C * KI) - (delta_motors_X*KS);
				PID_D +=(error_D * KI) + (delta_motors_Y*KS);		
				
				if (tick_remaining_A >0){					
					analogWrite(OUT_MOTOR_A, ZERO_SPEED + (PID_A)+ (error_A*KP));
				}
				else{
					stop_wheel(OUT_MOTOR_A);
				}
				if (tick_remaining_B >0){
					analogWrite(OUT_MOTOR_B, ZERO_SPEED + (PID_B)+ (error_B*KP));
				}
				else{
					stop_wheel(OUT_MOTOR_B);
				}
				if (tick_remaining_C >0){
					analogWrite(OUT_MOTOR_C, ZERO_SPEED + (PID_C)+ (error_C*KP));
				}
				else{
					stop_wheel(OUT_MOTOR_C);
				}
				if (tick_remaining_D >0){
					analogWrite(OUT_MOTOR_D, ZERO_SPEED + (PID_D)+ (error_D*KP));
				}
				else{
					stop_wheel(OUT_MOTOR_D);
				}		
				last_tick_remaining_A = tick_remaining_A;
				last_tick_remaining_B = tick_remaining_B;
				last_tick_remaining_C = tick_remaining_C;
				last_tick_remaining_D = tick_remaining_D;
				last_millis = millis();
			}		
		else{
			reset();
		}
	}
	else{
		reset();
	}
}

void start(){
	GO = true;
}
void stop(){
	GO = false;
}

// Stop a single wheel

void stop_wheel(int wheel){
	if (wheel == OUT_MOTOR_A){
		tick_remaining_A = 0;
		last_tick_remaining_A = 0;
		wanted_speed_A = 0;
		PID_A = 0;
		analogWrite(OUT_MOTOR_A, ZERO_SPEED);
		digitalWrite(PIN_ONE_MOTOR_A, LOW);
		digitalWrite(PIN_TWO_MOTOR_A, LOW);
		straight_X = false;
	}
	
	else if (wheel == OUT_MOTOR_B){
		tick_remaining_B = 0;
		last_tick_remaining_B = 0;
		wanted_speed_B = 0;
		PID_B = 0;
		analogWrite(OUT_MOTOR_A, ZERO_SPEED);
		digitalWrite(PIN_ONE_MOTOR_B, LOW);
		digitalWrite(PIN_TWO_MOTOR_B, LOW);
		straight_Y = false;
	}
	else if (wheel == OUT_MOTOR_C){
		tick_remaining_C = 0;
		last_tick_remaining_C = 0;
		wanted_speed_C = 0;
		PID_C = 0;
		analogWrite(OUT_MOTOR_A, ZERO_SPEED);
		digitalWrite(PIN_ONE_MOTOR_C, LOW);
		digitalWrite(PIN_TWO_MOTOR_C, LOW);
		straight_X = false;
	}
	else if(wheel == OUT_MOTOR_D){
		tick_remaining_D = 0;
		last_tick_remaining_D = 0;
		wanted_speed_D = 0;
		PID_D = 0;
		analogWrite(OUT_MOTOR_A, ZERO_SPEED);
		digitalWrite(PIN_ONE_MOTOR_D, LOW);
		digitalWrite(PIN_TWO_MOTOR_D, LOW);
		straight_Y = false;
		
	}
}


// reset and stop all wheels

void reset(){
	stop_wheel(OUT_MOTOR_A);
	stop_wheel(OUT_MOTOR_B);
	stop_wheel(OUT_MOTOR_C);
	stop_wheel(OUT_MOTOR_D);
	stop();
}

// ISR for every wheel encoder

void count_tick_A(){
	if(tick_remaining_A>0){
		tick_remaining_A--;
	}
}
void count_tick_B(){
	if (tick_remaining_B>0){
		tick_remaining_B--;
	}
}
void count_tick_C(){
	if (tick_remaining_C){
		tick_remaining_C--;
	}
}
void count_tick_D(){
	if (tick_remaining_D>0){
		tick_remaining_D--;
	}
}
