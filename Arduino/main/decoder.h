#ifndef decoder_h
#define decoder_h

#include "motors.h"


// DEFINE ALL THE DECODER HERE

// -------------SETUP ----------------
void decoder_init();


//-------------------------------------


bool decode_byte(int byte);

#endif // decoder.h