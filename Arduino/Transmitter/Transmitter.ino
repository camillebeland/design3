#include "manchester.h"

void setup() {
  // put your setup code here, to run once:
  manchester_init();
  Serial.begin(115200);

}

int time = 0;
int sum = 0;
int readbuff[32];
void loop() {
  // put your main code here, to run repeatedly:
    manchester_get();
    if (millis() - time > 1000){
      time = millis();
      manchester_read(readbuff);
      for (int i = 0; i<32; i++){
        Serial.print(readbuff[i]);
      }
    }
 }
    
