#ifndef serial_h
#define serial_h


#define BAUD_RATE 600

// -------------SETUP ----------------
void serial_init();


//-------------------------------------


int serial_send_manchester(int * ptr);

// ----------------ISR ----------------



#endif // serial_h