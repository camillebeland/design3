#ifndef magnet_h
#define magnet_h

#define OUT_MAGNET 30
#define IN_CAPACITOR_VOLTAGE 31 // MUST BE ADC
#define FULL_CAPACITOR_VOLTAGE 10

// -------------SETUP ----------------
void magnet_init();


//-------------------------------------

unsigned long get_capacitor_voltage();
void toggle_magnet(bool state);

// ----------------ISR ----------------



#endif // motors_h