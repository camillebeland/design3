#ifndef motors_h
#define motors_h

/*YELLOW = CH1
	BLUE = encoder power (5V)
	green = encoder GND
	RED = motor power +
	black = motor power -
	*/

#define INT_ENCODER_A_CH1 18 
#define INT_ENCODER_A_CH2 0

#define INT_ENCODER_B_CH1 19
#define INT_ENCODER_B_CH2 0

#define INT_ENCODER_C_CH1 20
#define INT_ENCODER_C_CH2 0

#define INT_ENCODER_D_CH1 21
#define INT_ENCODER_D_CH2 0

#define OUT_MOTOR_A 13
#define OUT_MOTOR_B 11
#define OUT_MOTOR_C 12
#define OUT_MOTOR_D 10

#define PIN_ONE_MOTOR_A 2
#define PIN_ONE_MOTOR_B 4
#define PIN_ONE_MOTOR_C 6
#define PIN_ONE_MOTOR_D 8

#define PIN_TWO_MOTOR_A 3
#define PIN_TWO_MOTOR_B 5
#define PIN_TWO_MOTOR_C 7
#define PIN_TWO_MOTOR_D 9

// 0 to 255
#define ZERO_SPEED 0

#define DT 100 // sec
#define DEFAULT_SPEED 100 // TICKS PER DT

#define KSI 0.02 // for delta motors
#define KSP 0.05
#define KI 0.02 // for PID
#define KP 0.1 //for PID

#define CRITICAL_TICK 256 // critical distance after what speed is reduced

#define LEFT 1
#define RIGHT 2
#define FORWARD 3
#define BACKWARD 4

// -------------SETUP ----------------
void motors_init();

//-------------------------------------
void start_motor(int motor);
void brake_motor(int motor);
void start();
void stop();
void set_motor(int motor, int tick, bool polarity, int motor_speed);
void reset_motor(int motor);
void reset_all_motors();
void move_straight(int direction, int tick, int speed);
void move(float angle, int tick, int speed);
void PID_motors();

// ----------------ISR ----------------

void count_tick_A();
void count_tick_B();
void count_tick_C();
void count_tick_D();

#endif // motors_h