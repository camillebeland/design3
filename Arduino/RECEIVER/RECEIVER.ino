char msg = ' '; //contains the message from arduino sender
const int led = 13; //led at pin 13
void setup() {
Serial.begin(9600);//Remember that the baud must be the same on both arduinos
pinMode(led,OUTPUT);
}
void loop() {
while(Serial.available()) {
           msg=Serial.read();
           if(msg=='H') {
               digitalWrite(led,HIGH);
           }
           if(msg=='L') {
                digitalWrite(led,LOW);
           }
delay(1000);
}
}
