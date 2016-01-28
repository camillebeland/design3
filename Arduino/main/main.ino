#include "motors.h"
#include "magnet.h"
#include "serial.h"
#include "decoder.h"

//int incomming_byte = -1;

void setup() {
  // put your setup code here, to run once:
  serial_init();
  //decoder_init();
  motors_init();
  //magnet_init();
  set_motor(OUT_MOTOR_A, 20000, true, 500);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  PID_motors();
//  incomming_byte = serial_read();
  //if (!decode_byte(incomming_byte)){
    //incomming_byte = -1;
  }
