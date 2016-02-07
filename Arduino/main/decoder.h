#ifndef decoder_h
#define decoder_h

#include "motors.h"


// DEFINE ALL THE DECODER HERE
#define START_CHAR '('
#define END_CHAR ')'

#define STOP_CHAR 's'
#define ROTATE_CHAR 'r'
#define MOVE_CHAR 'M'
#define MOVE_SLOW_CHAR 'm'

enum State {IDLE, FUNCTION, PARAMETERS, END};
enum Function {ROTATE, MOVE, STOP};

// -------------SETUP ----------------
void decoder_init();


//-------------------------------------


bool decode_byte(char byte);
bool parse_and_call();
#endif // decoder.h
