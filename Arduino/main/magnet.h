#ifndef magnet_h
#define magnet_h

#define OUT_MAGNET 22
#define IN_CAPACITOR_VOLTAGE  A0// MUST BE ADC
#define IN_BATTERY_VOLTAGE A1 // MUST BE ADC
#define FULL_CAPACITOR_VOLTAGE 10
#define ADC_N_VALUES 1024
#define BATTERY_MIN 0.5  // TO CHANGE
#define BATTERY_MAX 0.55

// -------------SETUP ----------------
void magnet_init();


//-------------------------------------

uint8_t get_capacitor_percent();
uint8_t get_battery_percent();
void toggle_magnet_ON();
void toggle_magnet_OFF();

// ----------------ISR ----------------



#endif