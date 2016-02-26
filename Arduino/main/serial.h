#ifndef serial_h
#define serial_h

#define BAUD_RATE 115200

// -------------SETUP ----------------
void serial_init();


//-------------------------------------


void serial_read();
void serial_print(char toPrint);

// ----------------ISR ----------------



#endif // serial_h