#include "motors.h"
#include "magnet.h"
#include "serial.h"
#include "decoder.h"

void setup() {
  // put your setup code here, to run once:
  serial_init();
  decoder_init();
  motors_init();
  //move_straight(FORWARD, 5000, DEFAULT_SPEED);
  //magnet_init();

  
}

void loop() {
  // put your main code here, to run repeatedly:
  PID_motors();
 if (Serial.available() >0){
    char incomming_byte = serial_read();
	  if (incomming_byte != -1){
		  decode_byte(incomming_byte);
    }
  }
 }
