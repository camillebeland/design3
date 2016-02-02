#include "motors.h"
#include "magnet.h"
#include "serial.h"
#include "decoder.h"

void setup() {
  // put your setup code here, to run once:
  serial_init();
  decoder_init();
  motors_init();
  //magnet_init();


}

void loop() {
  // put your main code here, to run repeatedly:
  PID_motors();
 
  char incomming_byte = serial_read();
	  if (!decode_byte(incomming_byte)){
		incomming_byte = -1;
	  }
  }
