#ifndef serial_h
#define serial_h

#define BAUD_RATE 115200

// -------------SETUP ----------------
void serial_init();


//-------------------------------------


void serial_read();
void serial_write(int toWrite);

// ----------------ISR ----------------



#endif // serial_h