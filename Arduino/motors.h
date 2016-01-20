#ifndef motors_h
#define motors_h


#define IN_ENCODER_1_CH1 1
#define IN_ENCODER_1_CH2 2

#define IN_ENCODER_2_CH1 3
#define IN_ENCODER_2_CH2 4

#define IN_ENCODER_3_CH1 5
#define IN_ENCODER_3_CH2 6

#define IN_ENCODER_4_CH1 7
#define IN_ENCODER_4_CH2 8

#define OUT_MOTOR_1 10
#define OUT_MOTOR_2 11
#define OUT_MOTOR_3 12
#define OUT_MOTOR_4 13

// 0 to 255
#define ZERO_SPEED 128
#define DEFAULT_SPEED 25
#define MAX_SPEED 100

#define LEFT 1
#define RIGHT 2
#define FORWARD 3
#define BACKWARD 4

void motor_init();

void move(int &direction, int & tick);


#endif // motors_h