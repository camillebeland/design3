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
int timestamp = 0;

void loop() {
  // put your main code here, to run repeatedly:
	serial_read();
  serial_manchester_read();
	PID_motors();
  if (millis() - timestamp > 1000){
    timestamp = millis();
    get_ASCII();
  }
}
 



