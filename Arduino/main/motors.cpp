#include "Arduino.h"
#include "motors.h"
#include <math.h> 


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
	pinMode(OUT_MOTOR_D, OUTPUT);
	
	pinMode(PIN_ONE_MOTOR_A, OUTPUT);
	pinMode(PIN_ONE_MOTOR_B, OUTPUT);
	pinMode(PIN_ONE_MOTOR_C, OUTPUT);
	pinMode(PIN_ONE_MOTOR_D, OUTPUT);
	
	pinMode(PIN_TWO_MOTOR_A, OUTPUT);
	pinMode(PIN_TWO_MOTOR_B, OUTPUT);
	pinMode(PIN_TWO_MOTOR_C, OUTPUT);
	pinMode(PIN_TWO_MOTOR_D, OUTPUT);

	digitalWrite(PIN_ONE_MOTOR_A, LOW);
	digitalWrite(PIN_ONE_MOTOR_B, LOW);
	digitalWrite(PIN_ONE_MOTOR_C, LOW);
	digitalWrite(PIN_ONE_MOTOR_D, LOW);
	
	digitalWrite(PIN_ONE_MOTOR_A, LOW);
	digitalWrite(PIN_TWO_MOTOR_B, LOW);
	digitalWrite(PIN_TWO_MOTOR_C, LOW);
	digitalWrite(PIN_TWO_MOTOR_D, LOW);
	
	analogWrite(OUT_MOTOR_A, 1);
	analogWrite(OUT_MOTOR_B, 1);	
	analogWrite(OUT_MOTOR_C, 1);	
	analogWrite(OUT_MOTOR_D, 1);	
	
	//setup timer3 for interrupt every DT (in microseconds);
	Timer3.initialize(DT*1000);
	Timer3.attachInterrupt(PID_motors_ISR());
	Timer3.stop();
	
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


//-------------------------------------------------------------------------------

//Configure the motor to start with the parameters previously set, starts PID
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
	//Starts PID
	Timer3.start();
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

// starts all motors with the parameters previously set, restart PID
void start(){
	start_motor(OUT_MOTOR_A);
	start_motor(OUT_MOTOR_B);
	start_motor(OUT_MOTOR_C);
	start_motor(OUT_MOTOR_D);
	Timer3.start();
}

//brake all motors, keeps the parameters, stops PID
void stop(){
	Timer3.stop();
	Timer3.reset();
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
	//Disable PID
	Timer3.stop();
}

// move forward, backward, left or right
void move_straight(Direction direction, int tick, int speed){
	
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
		set_motor(OUT_MOTOR_D, tick, true, speed);
		straight_Y = true;
	}
	else	if (direction == BACKWARD){
		set_motor(OUT_MOTOR_B, tick, true, speed);
		set_motor(OUT_MOTOR_D, tick, false, speed);
		straight_Y = true;
	}
	
}

// x = mm
// y = mm
void move(int x, int y, int speed){
	int ticks_X = x*TICKS_PER_MM;
	int ticks_Y = y*TICKS_PER_MM;
	float angle;
	if (x == 0 && y != 0){
		angle = PI/2;
	}
	else{
		angle = atan(abs(y)/abs(x));
	}
	int speed_X = cos(angle)*speed;
	int speed_Y = sin(angle)*speed;
	
	if (y >0){
		move_straight(FORWARD, ticks_Y, speed_Y);
	}
	else if (y < 0){
		move_straight(BACKWARD, ticks_Y, speed_Y);
	}
	
	if (ticks_X > 0){
		move_straight(RIGHT, ticks_X, speed_X);
	}
	else if (ticks_X < 0){
		move_straight(LEFT, ticks_X, speed_X);
	}

}

void rotate(Direction direction, int angle){
	int wanted_polarity;
	straight_X = true;
	straight_Y = true;
	if (direction == LEFT){
		wanted_polarity = true;
	}
	else if(direction == RIGHT){
		wanted_polarity = false;
	}
	int ticks = ROTATE_DIAMETER*PI*angle/360;
	
	set_motor(OUT_MOTOR_A, ticks, wanted_polarity, SLOW_SPEED);
	set_motor(OUT_MOTOR_B, ticks, wanted_polarity, SLOW_SPEED);
	set_motor(OUT_MOTOR_C, ticks, wanted_polarity, SLOW_SPEED);
	set_motor(OUT_MOTOR_D, ticks, wanted_polarity, SLOW_SPEED);
	
}

// PID for every wheel 
// TO DO -> modify regulator
// right now, comparing speeds of two wheel to go straight, apply feedback with the difference
// compute estimated position and compare to wanted final position
// will need testing on the physical robot
void PID_motors(){
	if (last_PID_ISR_count != PID_ISR_count){
		
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
		if (integrator_A > 255 - ZERO_SPEED){integrator_A = 255 - ZERO_SPEED;}
		integrator_B +=(error_B * KI);
		if (integrator_B > 255 - ZERO_SPEED){integrator_B = 255 - ZERO_SPEED;}
		integrator_C +=(error_C * KI);
		if (integrator_C > 255 - ZERO_SPEED){integrator_C = 255 - ZERO_SPEED;}
		integrator_D +=(error_D * KI);	
		if (integrator_D > 255 - ZERO_SPEED){integrator_D = 255 - ZERO_SPEED;}
		
		
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
			OCR5A = (ZERO_SPEED + (integrator_D) + (error_D*KP));// + (delta_motors_Y*KSP));
		}
		else{
			brake_motor(OUT_MOTOR_D);
			motors_done++;
		}		
		
		last_tick_remaining_A = tick_remaining_A;
		last_tick_remaining_B = tick_remaining_B;
		last_tick_remaining_C = tick_remaining_C;
		last_tick_remaining_D = tick_remaining_D;
		
		if (motors_done == 4){
			reset_all_motors();
		}
		last_PID_ISR_count = PID_ISR_count;
	}		
}

// ISR for calling PID_motors with Timer3 every DT
int PID_ISR_count = 0;
int last_PID_ISR_count = PID_ISR_count;
void PID_motors_ISR(){
	PID_ISR_count++;
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
