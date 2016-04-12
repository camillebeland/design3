#ifndef magnet_h
#define magnet_h

#define OUT_MAGNET 22
#define OUT_RECHARGE 24
#define OUT_DISCHARGE 26
#define IN_CAPACITOR_VOLTAGE  A0// MUST BE ADC
#define IN_BATTERY_VOLTAGE A1 // MUST BE ADC
#define FULL_CAPACITOR_VOLTAGE 2.6
#define ADC_N_VALUES 1024
#define BATTERY_MIN 3.7  	
#define BATTERY_MAX 4.2	

// -------------SETUP ----------------
void magnet_init();


//-------------------------------------

uint8_t get_capacitor_percent();
uint8_t get_battery_percent();
void toggle_magnet_ON();
void toggle_magnet_OFF();
void toggle_recharge_ON();
void toggle_recharge_OFF();
void toggle_discharge_ON();
void toggle_discharge_OFF();

// ----------------ISR ----------------



#endif