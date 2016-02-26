#ifndef serial_manchester_h
#define serial_manchester_h

#include "CircularBuffer.h"

#define BAUD_RATE_MANCHESTER 1200

// -------------SETUP ----------------
void serial_manchester_init();


//-------------------------------------


bool serial_manchester_read();
CircularBuffer get_manchester(int* ptr);
char get_ASCII();
// ----------------ISR ----------------



#endif // serial_manchester_h