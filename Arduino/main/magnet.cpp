#include "Arduino.h"
#include "magnet.h"

void magnet_init(){
	pinMode(OUT_MAGNET, OUTPUT);
	pinMode(IN_CAPACITOR_VOLTAGE, INPUT);
	pinMode(IN_BATTERY_VOLTAGE, INPUT);
	pinMode(OUT_RECHARGE, OUTPUT);
	pinMode(OUT_DISCHARGE, OUTPUT);
	digitalWrite(OUT_MAGNET, LOW);
}

void toggle_magnet_ON(){
	digitalWrite(OUT_MAGNET, HIGH);
}
void toggle_magnet_OFF(){
	digitalWrite(OUT_MAGNET, LOW);
}

void toggle_recharge_ON(){
	digitalWrite(OUT_RECHARGE, HIGH);
}

void toggle_recharge_OFF(){
	digitalWrite(OUT_RECHARGE, LOW);
}
void toggle_discharge_ON(){
	digitalWrite(OUT_DISCHARGE, HIGH);
}

void toggle_discharge_OFF(){
	digitalWrite(OUT_DISCHARGE, LOW);
}
uint8_t get_capacitor_percent(){
	int reading = (analogRead(IN_CAPACITOR_VOLTAGE) );
	double charge_fraction = (reading / double(ADC_N_VALUES)); // sur 5 V
	return (uint8_t)(3*(charge_fraction *100/5));
}
uint8_t get_battery_percent(){
	
	float min = BATTERY_MIN; // to change
	float max = BATTERY_MAX;
	float current = (analogRead(IN_BATTERY_VOLTAGE) /ADC_N_VALUES ) * 5;
	return (uint8_t)(100*(current - min) / (max-min));
}
