#ifndef serial_manchester_h
#define serial_manchester_h

#include "CircularBuffer.h"

#define BAUD_RATE_MANCHESTER 600

// -------------SETUP ----------------
void serial_manchester_init();


//-------------------------------------


void serial_manchester_read();
char get_ASCII();
int exp(int base, int power);
// ----------------ISR ----------------



#endif // serial_manchester_h