#ifndef motors_h
#define motors_h

/*YELLOW = CH1
	BLUE = encoder power (5V)
	green = encoder GND
	RED = motor power +
	black = motor power -
	*/
	
/*
Arduino Pin	Register
2					OCR3B
3					OCR3C
4					OCR4C
5					OCR3A
6					OCR4A
7					OCR4B
8					OCR4C
9					OCR2B
10					OCR2A
11					OCR1A
12					OCR1B
13					OCR0A
44					OCR5C
45					OCR5B
46					OCR5A

*/

#define INT_ENCODER_A_CH1 18
#define INT_ENCODER_A_CH2 0

#define INT_ENCODER_B_CH1 19
#define INT_ENCODER_B_CH2 0

#define INT_ENCODER_C_CH1 20
#define INT_ENCODER_C_CH2 0

#define INT_ENCODER_D_CH1 21
#define INT_ENCODER_D_CH2 0

#define OUT_MOTOR_A 13 // OCR0A
#define OUT_MOTOR_B 12 // OCR1B
#define OUT_MOTOR_C 44 // OCR5C
#define OUT_MOTOR_D 46 // OCR5A

#define PIN_ONE_MOTOR_A 53
#define PIN_ONE_MOTOR_B 49
#define PIN_ONE_MOTOR_C 45
#define PIN_ONE_MOTOR_D 41

#define PIN_TWO_MOTOR_A 51
#define PIN_TWO_MOTOR_B 47
#define PIN_TWO_MOTOR_C 43
#define PIN_TWO_MOTOR_D 39

#define ZERO_SPEED 37

#define DT 100000 //  microsecs
#define DEFAULT_SPEED 500 // TICKS PER DT
#define SLOW_SPEED 200
#define ROTATE_DIAMETER 1770//in TICKS

#define KSI 0.02 // for delta motors
#define KSP 0.1 // for delta motors
#define KI 0.02 // for speed PID
#define KP 0.1 //for speed PID

#define CRITICAL_TICK 256 // critical distance after what speed is reduced
#define TICKS_PER_MM 7.5

enum Direction {LEFT, RIGHT, FORWARD, BACKWARD};

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
void move_straight(Direction direction, int tick, int speed);
void move(int x, int y, int speed);
void rotate(Direction direction, int angle);
void PID_motors();

// ----------------ISR ----------------
void PID_motors_ISR();
void count_tick_A();
void count_tick_B();
void count_tick_C();
void count_tick_D();

#endif // motors_h
