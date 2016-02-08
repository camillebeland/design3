#ifndef decoder_h
#define decoder_h

#include "motors.h"


// DEFINE ALL THE DECODER HERE
#define START_CHAR '('
#define END_CHAR ')'

// STOP: (s)
// - s =  stop
// ROTATE: (rXY)
// - r = rotate.
// - X =  'l' or 'r' for left or right
// - Y = 8 bit value (angle) 0 to 255 (we only need 180 deg)
// MOVE SLOW or MOVE DEFAULT: (mXxYy) or (MXxYy)
// - m = move slow speed
// - M = move default speed
// - X = X axis MSBs (8 bits)
// - x = X axis LSB (8 bits) forming a 16 bit integer with 'X'
// - Y = Y axis MSBs (8 bits)
// - y = Y axis LSB (8 bits) forming a 16 bit integer with 'Y'




#define STOP_CHAR 's'
#define ROTATE_CHAR 'r'
#define MOVE_CHAR 'M'
#define MOVE_SLOW_CHAR 'm'

#define TIMEOUT 5000 //microsecs

enum State {IDLE, FUNCTION, PARAMETERS, END};
enum Function {MOVE, ROTATE, STOP};

// -------------SETUP ----------------
void decoder_init();


//-------------------------------------
void reset_decoder();
void decoder_tmeout();
bool decode_byte(char byte);
bool parse_and_call();

//-------------------------------------

void TIMEOUT_ISR();
#endif // decoder.h
