#include "motors.h"
#include "magnet.h"
#include "serial.h"
#include "decoder.h"
#include "serial_manchester.h"

void setup() {
  // put your setup code here, to run once:
	serial_init();
  serial_manchester_init();
	decoder_init();
	motors_init();
	magnet_init();
  //stop();
  
}

void loop() {
  // put your main code here, to run repeatedly:
	serial_read();
  // maybe put the manchester read on a timer intterupt!!!
  serial_manchester_read();
  //int hello = (int)get_ASCII();
  //serial_write(hello);
	PID_motors();

 }



