#include "manchester.h"
#include "serial.h"
void setup() {
  // put your setup code here, to run once:
  manchester_init();
  serial_init();
  delay(1000);
}
int readbuff[32];
void loop() {
    manchester_read(readbuff);
    serial_send_manchester(readbuff);
}
    
