#include "Arduino.h"
#include "magnet.h"

void magnet_init(){
	pinMode(OUT_MAGNET, OUTPUT);
	pinMode(IN_CAPACITOR_VOLTAGE, INPUT);
	digitalWrite(OUT_MAGNET, LOW);
}

void toggle_magnet_ON(){
	digitalWrite(OUT_MAGNET, HIGH);
}
void toggle_magnet_OFF(){
	digitalWrite(OUT_MAGNET, LOW);
}


float get_capacitor_voltage(){
	float charge_fraction = analogRead(IN_CAPACITOR_VOLTAGE) / ADC_N_VALUES;
	return charge_fraction * FULL_CAPACITOR_VOLTAGE;
}
