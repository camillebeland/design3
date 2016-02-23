#ifndef manchester_h
#define manchester_h

#define CLOCK_IN 2
#define MANCHESTER_IN 5

#define FREQUENCY  4900// Hz

// -------------SETUP ----------------
void manchester_init();


//-------------------------------------

void manchester_get();
void manchester_read(int * ptr);

//-------------------------------------

void CLOCK_ISR();

void MANCHESTER_ISR();
#endif // manchester.h
