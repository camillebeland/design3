#include "Arduino.h"
#include "magnet.h"

void magnet_init(){
	pinMode(OUT_MAGNET, OUTPUT);
	pinMode(IN_CAPACITOR_VOLTAGE, INPUT);
	digitalWrite(OUT_MAGNET, LOW);
}

void toggle_magnet(bool state){
	digitalWrite(OUT_MAGNET, HIGH);
}

unsigned long get_capacitor_voltage(){
	return (analogRead(IN_CAPACITOR_VOLTAGE)/1024) * FULL_CAPACITOR_VOLTAGE;
}
