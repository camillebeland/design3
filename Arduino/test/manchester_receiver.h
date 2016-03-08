#ifndef manchester_receiver_h
#define  manchester_receiver_h

#include "CircularBuffer.h"

#define BAUD_RATE_MANCHESTER 600

// -------------SETUP ----------------
void manchester_receiver_init();


//-------------------------------------


void manchester_receiver_read();
char get_ASCII();
bool checksum(int *ptr);
int exp(int base, int power);
// ----------------ISR ----------------



#endif // serial_manchester_h