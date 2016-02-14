#include "Arduino.h"
#include "motors.h"
#include <math.h> 
#include "TimerThree.h"


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
	Timer3.initialize(DT);
	Timer3.attachInterrupt(PID_motors_ISR);
	Timer3.stop();
	Timer3.restart();
	
}

//-------------------------------------------------------------------------------
// GLOBAL VARIABLES
long tick_remaining_A = 0;
long tick_remaining_B = 0;
long tick_remaining_C = 0;
long tick_remaining_D = 0;
long last_tick_remaining_A = 0;
long last_tick_remaining_B = 0;
long last_tick_remaining_C = 0;
long last_tick_remaining_D = 0;

bool polarity_A;
bool polarity_B;
bool polarity_C;
bool polarity_D;

double integrator_A = 0;
double integrator_B = 0;
double integrator_C = 0;
double integrator_D = 0;

bool running_A = false;
bool running_B = false;
bool running_C = false;
bool running_D = false;

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

int PID_ISR_count = 0;
int last_PID_ISR_count = PID_ISR_count;
int last_millis = millis();
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
			running_A = true;
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
			running_B = true;
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
			running_C = true;
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
			running_D = true;
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
		running_A = false;
	}
	
	else if (motor == OUT_MOTOR_B){
		digitalWrite(PIN_ONE_MOTOR_B, LOW);
		digitalWrite(PIN_TWO_MOTOR_B, LOW);
		straight_Y = false;
		integrator_B = 0;
		running_B = false;
	}
	else if (motor == OUT_MOTOR_C){
		digitalWrite(PIN_ONE_MOTOR_C, LOW);
		digitalWrite(PIN_TWO_MOTOR_C, LOW);
		straight_X = false;
		integrator_C = 0;
		running_C = false;
	}
	else if(motor == OUT_MOTOR_D){
		digitalWrite(PIN_ONE_MOTOR_D, LOW);
		digitalWrite(PIN_TWO_MOTOR_D, LOW);
		straight_Y = false;
		integrator_D = 0;
		running_D = false;
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
	Timer3.restart();
	brake_motor(OUT_MOTOR_A);
	brake_motor(OUT_MOTOR_B);
	brake_motor(OUT_MOTOR_C);
	brake_motor(OUT_MOTOR_D);
}

//set parameters for a specific wheel/motor
void set_motor(int motor, int tick, bool polarity, double motor_speed){
	
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
void move_straight(Direction direction, int tick, double speed){
	
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
// MSB = negative
void move(int x, int y, double speed){
	
	int ticks_X = x*TICKS_PER_MM;
	int ticks_Y = y*TICKS_PER_MM;
	float angle;
	if (x == 0 && y != 0){
		angle = PI/2;
	}
	else{
		angle = atan(abs(y)/abs(x));
	}
	double speed_X = cos(angle)*speed;
	double speed_Y = sin(angle)*speed;
	
	if (y <32768){
		move_straight(FORWARD, ticks_Y, speed_Y);
	}
	else if (y >= 32768){
		move_straight(BACKWARD, ticks_Y, speed_Y);
	}
	
	if (ticks_X < 32768){
		move_straight(RIGHT, ticks_X, speed_X);
	}
	else if (ticks_X >= 32768){
		move_straight(LEFT, ticks_X, speed_X);
	}

}

void rotate(Direction direction, int angle){
	int wanted_polarity;

	if (direction == LEFT){
		wanted_polarity = true;
	}
	else if(direction == RIGHT){
		wanted_polarity = false;
	}
	int ticks = ROTATE_DIAMETER*PI*angle/360;
	
	set_motor(OUT_MOTOR_A, ticks, wanted_polarity, ROTATE_SPEED);
	set_motor(OUT_MOTOR_B, ticks, wanted_polarity, ROTATE_SPEED);
	set_motor(OUT_MOTOR_C, ticks, wanted_polarity, ROTATE_SPEED);
	set_motor(OUT_MOTOR_D, ticks, wanted_polarity, ROTATE_SPEED);
	straight_X = true;
	straight_Y = true;
	
}

// PID for every wheel 
// TO DO -> modify regulator
// right now, comparing speeds of two wheel to go straight, apply feedback with the difference
// compute estimated position and compare to wanted final position
// will need testing on the physical robot
void PID_motors(){
	if (last_PID_ISR_count != PID_ISR_count){
		int dt = millis() - last_millis;
		//speed is tick/dt		last_millis = millis();
/*		Serial.print(actual_speed_A);
		Serial.print("\t");
		Serial.print(actual_speed_B);
		Serial.print("\t");
		Serial.print(actual_speed_C);
		Serial.print("\t");
		Serial.print(actual_speed_D);
		Serial.print("\n");*/
		
		//Serial.println(tick_remaining_A);
		actual_speed_A = 1000000*(last_tick_remaining_A - tick_remaining_A)/(DT);
		actual_speed_B = 1000000*(last_tick_remaining_B - tick_remaining_B)/(DT);
		actual_speed_C = 1000000*(last_tick_remaining_C - tick_remaining_C)/(DT);
		actual_speed_D = 1000000*(last_tick_remaining_D - tick_remaining_D)/(DT);
		last_tick_remaining_A = tick_remaining_A;
		last_tick_remaining_B = tick_remaining_B;
		last_tick_remaining_C = tick_remaining_C;
		last_tick_remaining_D = tick_remaining_D;
		
		
		// Error = difference to wanted speed
		double error_A = wanted_speed_A - actual_speed_A;
		double error_B = wanted_speed_B - actual_speed_B;
		double error_C = wanted_speed_C - actual_speed_C;
		double error_D = wanted_speed_D - actual_speed_D;				
		
		double delta_motors_X = 0;
		if (straight_X){
			delta_motors_X =  actual_speed_A  - actual_speed_C ;
		}
		double delta_motors_Y = 0;
		if (straight_Y){
			
			delta_motors_Y =actual_speed_B - actual_speed_D;
		}
		
		integrator_A +=(error_A * KI)- (delta_motors_X*KSI);
		if (integrator_A > 255 - ZERO_SPEED){integrator_A = 255 - ZERO_SPEED;}
		integrator_B +=(error_B * KI)- (delta_motors_Y*KSI) ;
		if (integrator_B > 255 - ZERO_SPEED){integrator_B = 255 - ZERO_SPEED;}
		integrator_C +=(error_C * KI);
		if (integrator_C > 255 - ZERO_SPEED){integrator_C = 255 - ZERO_SPEED;}
		integrator_D +=(error_D * KI);	
		if (integrator_D > 255 - ZERO_SPEED){integrator_D = 255 - ZERO_SPEED;}
		
		int command = 0;
		if (tick_remaining_A >0){	
			command = ((ZERO_SPEED + (integrator_A) + (error_A*KP))- (delta_motors_X*KSP)) ;
			
			OCR0A = limit_command(command);;
		}
		else if (running_A){
			brake_motor(OUT_MOTOR_A);
		}
		if (tick_remaining_B >0){
			 command = ((ZERO_SPEED + (integrator_B) + (error_B*KP)) - (delta_motors_Y*KSP));
			 OCR1B = limit_command(command);
		}
		else if (running_B){
			brake_motor(OUT_MOTOR_B);
		}
		
		if (tick_remaining_C >0){
			command = (ZERO_SPEED + (integrator_C) + (error_C*KP));//+ (delta_motors_X*KSP) ;
			OCR5C = limit_command(command);
		}
		else if (running_C){
			brake_motor(OUT_MOTOR_C);
		}
		if (tick_remaining_D >0){
			command = (ZERO_SPEED + (integrator_D) + (error_D*KP));// + (delta_motors_Y*KSP);
			OCR5A = limit_command(command);
		}
		else if (running_D){
			brake_motor(OUT_MOTOR_D);
		}		
		
		if (!running_A && !running_B && !running_C && !running_D){
			reset_all_motors();
		}
		
		last_PID_ISR_count = PID_ISR_count;
	}		
}

int limit_command(double command){
	if (command >= 255){return 255;}
	else if(command <= 0){return 0;}
	else{return command;}
}

// ISR for calling PID_motors with Timer3 every DT
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
