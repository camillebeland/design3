#include "motors.h"
#include "magnet.h"
#include "serial.h"
#include "decoder.h"
#include "manchester_receiver.h"

void setup() {
  // put your setup code here, to run once:
	serial_init();
  manchester_receiver_init();
	decoder_init();
	motors_init();
	magnet_init();
  //stop();
  
}
int timestamp = 0;

void loop() {
  // put your main code here, to run repeatedly:
	serial_read();
  // maybe put the manchester read on a timer intterupt!!!
  manchester_receiver_read();
  //int hello = (int)get_ASCII();
  //serial_write(hello);
	PID_motors();
  if (millis() - timestamp > 1000){
    timestamp = millis();
    get_ASCII();
  }
}
 



