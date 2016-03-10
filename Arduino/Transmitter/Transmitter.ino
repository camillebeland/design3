#include "manchester.h"
#include "serial.h"
void setup() {
  // put your setup code here, to run once:
  manchester_init();
  serial_init();
  Serial.begin(115200); // debug
  //delay(1000);
}
int readbuff[32];
void loop() {
    manchester_read(readbuff);
    for(int i =0 ; i<32; i++){
      Serial.print(readbuff[i]);
    }
    Serial.println(" - ");
    serial_send_manchester(readbuff);
}
    
