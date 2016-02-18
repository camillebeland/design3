#ifndef magnet_h
#define magnet_h

#define OUT_MAGNET 22
#define IN_CAPACITOR_VOLTAGE  A0// MUST BE ADC
#define FULL_CAPACITOR_VOLTAGE 10
#define ADC_N_VALUES 1024

// -------------SETUP ----------------
void magnet_init();


//-------------------------------------

float get_capacitor_voltage();
void toggle_magnet_ON();
void toggle_magnet_OFF();

// ----------------ISR ----------------



#endif // motors_h