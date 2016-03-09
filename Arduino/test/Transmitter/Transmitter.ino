#include "manchester.h"
#include "manchester_transmitter.h"
void setup() {
  // put your setup code here, to run once:
  manchester_init();
  manchester_transmitter_init();
  Serial.begin(115200);
  //delay(1000);
}
int readbuff[32];
void loop() {
    manchester_read(readbuff);
    /*for(int i =0 ; i<32; i++){
      Serial.print(readbuff[i]);
    }
    Serial.println(" - ");
*/    manchester_transmitter_send(readbuff);
}
    
