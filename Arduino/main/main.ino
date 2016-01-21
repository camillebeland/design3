#include "motors.h"

void setup() {
  // put your setup code here, to run once:
  motor_init();
  move_straight(FORWARD, 100, DEFAULT_SPEED);
  move_straight(RIGHT, 100, DEFAULT_SPEED);
}

void loop() {
  // put your main code here, to run repeatedly:
  PID_motors();
}
