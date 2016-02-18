#ifndef serial_h
#define serial_h

#define RX 0
#define TX 0

#define BAUD_RATE 115200

// -------------SETUP ----------------
void serial_init();


//-------------------------------------


int serial_read();

// ----------------ISR ----------------



#endif // serial_h