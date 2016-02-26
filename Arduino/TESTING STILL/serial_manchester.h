#ifndef serial_manchester_h
#define serial_manchester_h

#define RX 19
#define TX 18

#define BAUD_RATE 1200

// -------------SETUP ----------------
void serial_manchester_init();


//-------------------------------------


bool serial_manchester_read();
CircularBuffer get_manchester(int* ptr);
void serial_manchester_send(char code);
// ----------------ISR ----------------



#endif // serial_manchester_h