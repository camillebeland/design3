void setup() {
delay(1000);
Serial.begin(9600);
delay(1000);
}
void loop() {
Serial.println("H"); //turn on the LED
delay(1000);
Serial.println("L");//turn off the LED
delay(1000);
}
