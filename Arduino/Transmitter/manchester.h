#ifndef manchester_h
#define manchester_h

#define CLOCK_IN 3
#define MANCHESTER_IN 6

#define FREQUENCY  4900// Hz

// -------------SETUP ----------------
void manchester_init();


//-------------------------------------

void manchester_read(int * ptr);

//-------------------------------------

void CLOCK_ISR();

void MANCHESTER_ISR();
#endif // manchester.h
