#ifndef motors_h
#define motors_h

#define INT_ENCODER_A_CH1 2
#define INT_ENCODER_A_CH2 0

#define INT_ENCODER_B_CH1 3
#define INT_ENCODER_B_CH2 0

#define INT_ENCODER_C_CH1 18
#define INT_ENCODER_C_CH2 0

#define INT_ENCODER_D_CH1 19
#define INT_ENCODER_D_CH2 0

#define OUT_MOTOR_A 10
#define OUT_MOTOR_B 11
#define OUT_MOTOR_C 12
#define OUT_MOTOR_D 13

#define POLARITY_MOTOR_A 20
#define POLARITY_MOTOR_B 21
#define POLARITY_MOTOR_C 22
#define POLARITY_MOTOR_D 23

#define ACTIVATION_MOTOR_A 24
#define ACTIVATION_MOTOR_B 25
#define ACTIVATION_MOTOR_C 26
#define ACTIVATION_MOTOR_D 27

// 0 to 255
#define ZERO_SPEED 128

#define DT 0.2 // sec
#define DEFAULT_SPEED 100 // TICKS PER DT

#define KS 1 // for delta motors
#define KI 1 // for PID

#define CRITICAL_TICK 256 // critical distance after what speed is reduced

#define LEFT 1
#define RIGHT 2
#define FORWARD 3
#define BACKWARD 4

// -------------SETUP ----------------
void motor_init();


//-------------------------------------
void move(float angle, int tick, int speed);
void move_wheel(int wheel, int wheel_tick, int polarity,  int wheel_speed);
void stop_wheel(int motor);
void move_straight(int direction, int tick, int speed);
void PID_motors();
void reset();
void start();
void stop();



// ----------------ISR ----------------

void count_tick_A();
void count_tick_B();
void count_tick_C();
void count_tick_D();

#endif // motors_h