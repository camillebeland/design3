#ifndef manchester_transmitter_h
#define manchester_transmitter_h


#define BAUD_RATE 600
#define TX_PIN 18

// -------------SETUP ----------------
void manchester_transmitter_init();


//-------------------------------------


int manchester_transmitter_send(int * ptr);

// ----------------ISR ----------------



#endif // serial_h