#include "Arduino.h"
#include "magnet.h"

void magnet_init(){
	pinMode(OUT_MAGNET, OUTPUT);
	pinMode(IN_CAPACITOR_VOLTAGE, INPUT);
	pinMode(IN_BATTERY_VOLTAGE, INPUT);
	digitalWrite(OUT_MAGNET, LOW);
}

void toggle_magnet_ON(){
	digitalWrite(OUT_MAGNET, HIGH);
}
void toggle_magnet_OFF(){
	digitalWrite(OUT_MAGNET, LOW);
}


uint8_t get_capacitor_percent(){
	float charge_fraction = (analogRead(IN_CAPACITOR_VOLTAGE) / ADC_N_VALUES); // sur 5 V
	return (uint8_t)charge_fraction *100;
}
uint8_t get_battery_percent(){
	
	float min = BATTERY_MIN; // to change
	float max = BATTERY_MAX;
	float current = (analogRead(IN_BATTERY_VOLTAGE) /ADC_N_VALUES ) * 5;
	return (uint8_t)(100*(current - min) / (max-min));
}
