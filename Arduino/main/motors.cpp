#include "Arduino.h"
#include "motors.h"

void motors_init(){
	pinMode(INT_ENCODER_A_CH1, INPUT);
	pinMode(INT_ENCODER_B_CH1, INPUT);
	pinMode(INT_ENCODER_C_CH1, INPUT);
	pinMode(INT_ENCODER_D_CH1, INPUT);

	attachInterrupt(digitalPinToInterrupt(INT_ENCODER_A_CH1), count_tick_A, RISING);
	attachInterrupt(digitalPinToInterrupt(INT_ENCODER_B_CH1), count_tick_B, RISING);
	attachInterrupt(digitalPinToInterrupt(INT_ENCODER_C_CH1), count_tick_C, RISING);
	attachInterrupt(digitalPinToInterrupt(INT_ENCODER_D_CH1), count_tick_D, RISING);	
	
	pinMode(OUT_MOTOR_A, OUTPUT);
	pinMode(OUT_MOTOR_B, OUTPUT);
	pinMode(OUT_MOTOR_C, OUTPUT);
	//pinMode(OUT_MOTOR_D, OUTPUT);
	
	pinMode(PIN_ONE_MOTOR_A, OUTPUT);
	pinMode(PIN_ONE_MOTOR_B, OUTPUT);
	pinMode(PIN_ONE_MOTOR_C, OUTPUT);
	//pinMode(PIN_ONE_MOTOR_D, OUTPUT);
	
	pinMode(PIN_TWO_MOTOR_A, OUTPUT);
	pinMode(PIN_TWO_MOTOR_B, OUTPUT);
	pinMode(PIN_TWO_MOTOR_C, OUTPUT);
	//pinMode(PIN_TWO_MOTOR_D, OUTPUT);

	digitalWrite(PIN_ONE_MOTOR_A, LOW);
	digitalWrite(PIN_ONE_MOTOR_B, LOW);
	digitalWrite(PIN_ONE_MOTOR_C, LOW);
	//digitalWrite(PIN_ONE_MOTOR_D, LOW);
	
	digitalWrite(PIN_ONE_MOTOR_A, LOW);
	digitalWrite(PIN_TWO_MOTOR_B, LOW);
	digitalWrite(PIN_TWO_MOTOR_C, LOW);
	//digitalWrite(PIN_TWO_MOTOR_D, LOW);
	
	analogWrite(OUT_MOTOR_A, 1);
	analogWrite(OUT_MOTOR_B, 10);	
	analogWrite(OUT_MOTOR_C, 1);	
	//analogWrite(OUT_MOTOR_D, 10);	
	
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

double integrator_A = 0;
double integrator_B = 0;
double integrator_C = 0;
double integrator_D = 0;

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

bool running = false;
double dt;

//-------------------------------------------------------------------------------

//Configure the motor to start with the parameters previously set
void start_motor(int motor){
	if (motor == OUT_MOTOR_A){
		if (tick_remaining_A>0){
			if (polarity_A){
				
				digitalWrite(PIN_ONE_MOTOR_A, HIGH);
				digitalWrite(PIN_TWO_MOTOR_A, LOW);
			}
			else{
				digitalWrite(PIN_ONE_MOTOR_A, LOW);
				digitalWrite(PIN_TWO_MOTOR_A,  HIGH);		
			}
		}
	}
	else if (motor == OUT_MOTOR_B){
		if (tick_remaining_B>0){
			if (polarity_B){
				digitalWrite(PIN_ONE_MOTOR_B, HIGH);
				digitalWrite(PIN_TWO_MOTOR_B, LOW);
			}
			else{
				digitalWrite(PIN_ONE_MOTOR_B, LOW);
				digitalWrite(PIN_TWO_MOTOR_B,  HIGH);		
			}
		}
	}
	else if (motor == OUT_MOTOR_C){
		if (tick_remaining_C>0){
			if (polarity_C){
				digitalWrite(PIN_ONE_MOTOR_C, HIGH);
				digitalWrite(PIN_TWO_MOTOR_C, LOW);
			}
			else{
				digitalWrite(PIN_ONE_MOTOR_C, LOW);
				digitalWrite(PIN_TWO_MOTOR_C,  HIGH);		
			}
		}
	}
	else if (motor == OUT_MOTOR_D){
		if (tick_remaining_D>0){
			if (polarity_D){
				digitalWrite(PIN_ONE_MOTOR_D, HIGH);
				digitalWrite(PIN_TWO_MOTOR_D, LOW);
			}
			else{
				digitalWrite(PIN_ONE_MOTOR_D, LOW);
				digitalWrite(PIN_TWO_MOTOR_D,  HIGH);		
			}
		}
	}
}

// stops a single motor
void brake_motor(int motor){
	if (motor == OUT_MOTOR_A){
		digitalWrite(PIN_ONE_MOTOR_A, LOW);
		digitalWrite(PIN_TWO_MOTOR_A, LOW);
		straight_X = false;
		integrator_A = 0;
	}
	
	else if (motor == OUT_MOTOR_B){
		digitalWrite(PIN_ONE_MOTOR_B, LOW);
		digitalWrite(PIN_TWO_MOTOR_B, LOW);
		straight_Y = false;
		integrator_B = 0;
	}
	else if (motor == OUT_MOTOR_C){
		digitalWrite(PIN_ONE_MOTOR_C, LOW);
		digitalWrite(PIN_TWO_MOTOR_C, LOW);
		straight_X = false;
		integrator_C = 0;
	}
	else if(motor == OUT_MOTOR_D){
		digitalWrite(PIN_ONE_MOTOR_D, LOW);
		digitalWrite(PIN_TWO_MOTOR_D, LOW);
		straight_Y = false;
		integrator_D = 0;
	}
}

// starts all motors with the parameters previously set
void start(){
	running = true;
	last_millis = millis();
	start_motor(OUT_MOTOR_A);
	start_motor(OUT_MOTOR_B);
	start_motor(OUT_MOTOR_C);
	start_motor(OUT_MOTOR_D);
}

//brake all motors, keeps the parameters
void stop(){
	running = false;
	brake_motor(OUT_MOTOR_A);
	brake_motor(OUT_MOTOR_B);
	brake_motor(OUT_MOTOR_C);
	brake_motor(OUT_MOTOR_D);
}

//set parameters for a specific wheel/motor
void set_motor(int motor, int tick, bool polarity, int motor_speed){
	
	if (motor == OUT_MOTOR_A){
		tick_remaining_A =tick;
		last_tick_remaining_A = tick;
		wanted_speed_A= motor_speed;
		polarity_A = polarity;
		start_motor(OUT_MOTOR_A);
		straight_X = false;
	}
	else if(motor == OUT_MOTOR_B){
		tick_remaining_B = tick;
		last_tick_remaining_B = tick;
		wanted_speed_B = motor_speed;
		polarity_B = polarity;
		start_motor(OUT_MOTOR_B);
		straight_Y = false;
	}
	else if (motor == OUT_MOTOR_C){
		tick_remaining_C = tick;
		last_tick_remaining_C = tick;
		wanted_speed_C= motor_speed;
		polarity_C = polarity;
		start_motor(OUT_MOTOR_C);
		straight_X = false;
	}
	else if(motor == OUT_MOTOR_D){
		tick_remaining_D = tick;
		last_tick_remaining_D = tick;
		wanted_speed_D= motor_speed;
		polarity_D = polarity;
		start_motor(OUT_MOTOR_D);
		straight_Y = false;
	}
	running = true;
}

//reset parameters and stop a single motor
void reset_motor(int motor){
	if (motor == OUT_MOTOR_A){
		tick_remaining_A = 0;
		last_tick_remaining_A = 0;
		wanted_speed_A = 0;
		integrator_A = 0;
		brake_motor(OUT_MOTOR_A);
	}
	
	else if (motor == OUT_MOTOR_B){
		tick_remaining_B = 0;
		last_tick_remaining_B = 0;
		wanted_speed_B = 0;
		integrator_B = 0;
		brake_motor(OUT_MOTOR_B);
	}
	else if (motor == OUT_MOTOR_C){
		tick_remaining_C = 0;
		last_tick_remaining_C = 0;
		wanted_speed_C = 0;
		integrator_C = 0;
		brake_motor(OUT_MOTOR_C);
	}
	else if(motor == OUT_MOTOR_D){
		tick_remaining_D = 0;
		last_tick_remaining_D = 0;
		wanted_speed_D = 0;
		integrator_D = 0;
		brake_motor(OUT_MOTOR_D);
	}
}

// reset and stop all motors
void reset_all_motors(){
	reset_motor(OUT_MOTOR_A);
	reset_motor(OUT_MOTOR_B);
	reset_motor(OUT_MOTOR_C);
	reset_motor(OUT_MOTOR_D);
	running = false;
}

// move forward, backward, left or right
void move_straight(int direction, int tick, int speed){
	
	//set movement parameters, choose the appropriate motors to use
	if (direction == LEFT){
		set_motor(OUT_MOTOR_A, tick, true, speed);
		set_motor(OUT_MOTOR_C, tick, false, speed);
		straight_X = true;
	}
	else if (direction == RIGHT){
		set_motor(OUT_MOTOR_A, tick, false, speed);
		set_motor(OUT_MOTOR_C, tick, true, speed);
		straight_X = true;
	}
	else if (direction == FORWARD){
		set_motor(OUT_MOTOR_B, tick, false, speed);
		//set_motor(OUT_MOTOR_D, tick, true, speed);
		straight_Y = true;
	}
	else	if (direction == BACKWARD){
		set_motor(OUT_MOTOR_B, tick, true, speed);
		//set_motor(OUT_MOTOR_D, tick, false, speed);
		straight_Y = true;
	}
	
}

void rotate(int direction, int angle){
	int wanted_polarity;
	straight_X = true;
	straight_Y = true;
	if (direction == LEFT){
		wanted_polarity = true;
	}
	else if(direction == RIGHT){
		wanted_polarity = false;
	}
	int ticks = ROTATE_DIAMETER*PI*(float(angle)/360);
	
	set_motor(OUT_MOTOR_A, ticks, wanted_polarity, DEFAULT_SPEED);
	set_motor(OUT_MOTOR_B, ticks, wanted_polarity, DEFAULT_SPEED);
	set_motor(OUT_MOTOR_C, ticks, wanted_polarity, DEFAULT_SPEED);
	//set_motor(OUT_MOTOR_D, ticks, wanted_polarity, DEFAULT_SPEED);
	
}

// PID for every wheel 
// TO DO -> modify regulator
// right now, comparing speeds of two wheel to go straight, apply feedback with the difference
// compute estimated position and compare to wanted final position
// will need testing on the physical robot
//bool connected_A = false;
//bool connected_C = false;
void PID_motors(){
	
	if (running){
		
			dt = millis() - last_millis;
			if (dt >= DT){
				
				//speed is tick/dt
				actual_speed_A = (last_tick_remaining_A - tick_remaining_A)/(dt/1000);
				actual_speed_B = (last_tick_remaining_B - tick_remaining_B)/(dt/1000);
				actual_speed_C = (last_tick_remaining_C - tick_remaining_C)/(dt/1000);
				actual_speed_D = (last_tick_remaining_D - tick_remaining_D)/(dt/1000);
				
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
				
				integrator_A +=(error_A * KI);
				integrator_B +=(error_B * KI);
				integrator_C +=(error_C * KI);
				integrator_D +=(error_D * KI);	
				
				
				int motors_done = 0;

				if (tick_remaining_A >0){	
					OCR0A = ZERO_SPEED + (integrator_A) + (error_A*KP)-(delta_motors_X*KSP);
				}
				else{
					brake_motor(OUT_MOTOR_A);
					motors_done++;
				}
				if (tick_remaining_B >0){
					OCR1B = (ZERO_SPEED + (integrator_B) + (error_B*KP));// - (delta_motors_Y*KSP) );
				}
				else{
					brake_motor(OUT_MOTOR_B);
					motors_done++;
				}
				
				if (tick_remaining_C >0){
					OCR5C = (ZERO_SPEED + (integrator_C) + (error_C*KP)) +(delta_motors_X*KSP);
				}
				else{
					brake_motor(OUT_MOTOR_C);
					motors_done++;
				}
				if (tick_remaining_D >0){
					OCR0A = (ZERO_SPEED + (integrator_D) + (error_D*KP));// + (delta_motors_Y*KSP));
				}
				else{
					brake_motor(OUT_MOTOR_D);
					motors_done++;
				}		
				
				last_tick_remaining_A = tick_remaining_A;
				last_tick_remaining_B = tick_remaining_B;
				last_tick_remaining_C = tick_remaining_C;
				last_tick_remaining_D = tick_remaining_D;
				last_millis = millis();
				
				if (motors_done == 4){
					reset_all_motors();
				}
			}		
	}
}

// ISR for every wheel encoder

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
