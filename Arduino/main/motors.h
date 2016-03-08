#ifndef motors_h
#define motors_h

/*YELLOW = CH1
	BLUE = encoder power (5V)
	green = encoder GND
	RED = motor power +
	black = motor power -
	*/
	
/*  PWM DUTY CYCLE
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
#define OUT_MOTOR_B 45 // OCR5B
#define OUT_MOTOR_C 46 // OCR5C
#define OUT_MOTOR_D 44 // OCR5A

#define PIN_ONE_MOTOR_A 53
#define PIN_ONE_MOTOR_B 49
#define PIN_ONE_MOTOR_C 43
#define PIN_ONE_MOTOR_D 39

#define PIN_TWO_MOTOR_A 51
#define PIN_TWO_MOTOR_B 47
#define PIN_TWO_MOTOR_C 41
#define PIN_TWO_MOTOR_D 37

#define ZERO_SPEED 50 // PWM COMMAND for near start

#define FREQ 20 //  Hz
#define DEFAULT_SPEED 1000 // TICKS PER SEC
#define SLOW_SPEED 500
#define ROTATE_SPEED 500
#define ROTATE_DIAMETER 195.56 //mm

#define KSI 0.0075 // for delta motors
#define KSP 0.015// for delta motors
#define KI 0.03 // for speed PID
#define KP 0.05 //for speed PID

#define TICKS_PER_MM 15.34	 //  including slip 
#define WHEEL_DIAMETER 69.85 //mm

enum Direction {LEFT, RIGHT, FORWARD, BACKWARD};

// -------------SETUP ----------------
void motors_init();

//-------------------------------------
void start_motor(int motor);
void brake_motor(int motor);
void start();
void stop();
void set_motor(int motor, long tick, bool polarity, double motor_speed);
void reset_motor(int motor);
void reset_all_motors();
void move_straight(Direction direction, long tick, double speed);
void move(long x, long y, double speed);
void rotate(Direction direction, int angle);
void PID_motors();
int limit_command(double command);

void test();

// ----------------ISR ----------------
void PID_motors_ISR();
void count_tick_A();
void count_tick_B();
void count_tick_C();
void count_tick_D();

#endif // motors_h
