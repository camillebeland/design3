#include "Arduino.h"
#include "decoder.h"
#include "motors.h"
#include "TimerFour.h"
#include "serial_manchester.h"
#include "serial.h"
#include "magnet.h"

void decoder_init() {
  Timer4.init(TIMEOUT_FREQ,TIMEOUT_ISR);
  Timer4.stop();
}

State current_state = IDLE;
Function current_function;
int speed_param = DEFAULT_SPEED;
int param_count = 0;
int params[4] = {0};

void reset_decoder() {
  Timer4.stop();
  current_state = IDLE;
}

bool decode_byte(unsigned char byte) {

  bool byte_decoded = false;

  if (byte == START_CHAR and current_state != PARAMETERS) {
    reset_decoder;
  };

  switch (current_state) {

    case IDLE:
      if (byte == START_CHAR) {
        current_state = FUNCTION;
        byte_decoded = true;
        param_count = 0;
        Timer4.start();
      }
      else {
        byte_decoded = false;
      }
      break;

    case FUNCTION:
      byte_decoded = true;
      if (byte == 's') {
        current_function = STOP;
        current_state = END;
      }
      else if (byte == 'm' || byte == 'M') {
        current_function = MOVE;
        param_count = 4;
        if (byte == 'm') {
          speed_param = SLOW_SPEED;
        }
        else {
          speed_param = DEFAULT_SPEED;
        }
        current_state = PARAMETERS;
      }
      else if (byte == 'r') {
        current_function = ROTATE;
        param_count = 2;
        current_state = PARAMETERS;
      }
      else if (byte == 'a') {
        current_function = MAGNET;
        param_count = 1;
        current_state = PARAMETERS;
      }
	  else if(byte == 'c'){
		current_function = MANCHESTER;
		param_count = 0;
		current_state = END;
	  }
	  else if(byte == 't'){
		current_function = TEST;
		param_count = 0;
		current_state = END;
	  }
	  else if(byte == 'b'){
		current_function = BATTERY;
		param_count = 0;
		current_state = END;
	  }
	  else if (byte == 'v'){
		current_function = MAGNET_VOLTAGE;
		param_count = 0;
		current_state = END;
	  }
	  
      // cover errors
      else {
        byte_decoded = false;
        current_state = IDLE;
      }
      break;

    case PARAMETERS:
      byte_decoded = true;
      if (param_count > 0) {
        params[4 - param_count] = byte;
        param_count--;
      }
      if (param_count < 1) {
        byte_decoded = true;
        current_state = END;
      }
      break;

    case END:
      byte_decoded = true;
      if (byte == END_CHAR) {
        parse_and_call();
      }
      else {
        byte_decoded = false;
      }
      reset_decoder();
      break;

    default:
      reset_decoder()
      break;

  }
  return byte_decoded;
}

bool parse_and_call() {

  long angle, x, y;
  char ONOFF;
  long buffa, buffb, buffc, buffd;
  switch (current_function) {
    case STOP:
      stop();
      break;

    case ROTATE:
      Direction direction;
      if (params[2] == 'l') {
        direction = LEFT;
      }
      else if (params[2] == 'r') {
        direction = RIGHT;
      }
      else {
        return false;
      }
      angle = int(params[3]);
      rotate(direction, angle);
      break;

    case MOVE:
		buffa = (long)params[0];
		buffb = (long)params[1];
		buffc = (long)params[2];
		buffd = (long)params[3];
		x = (buffa << 8)+ buffb;
		y = (buffc << 8)+ buffd;
      move(x, y, speed_param);
      break;

    case MAGNET:
      ONOFF = params[3];
      if (ONOFF == 'o') {
        toggle_magnet_ON();
      }
      else if (ONOFF == 'f') {
        toggle_magnet_OFF();
      }
	  else if(ONOFF == 'c'){
		toggle_recharge_ON();
	  }
	  else if(ONOFF == 'd'){
		toggle_recharge_OFF();
	  }
	  else if(ONOFF == 'x'){
		toggle_discharge_ON();
		toggle_magnet_ON();
	  }
	  else if(ONOFF == 'z'){
		toggle_discharge_OFF();
		toggle_magnet_OFF();
	  }
	  break;
	case MANCHESTER:
		serial_write(get_ASCII());
		break;
	case MAGNET_VOLTAGE:
		serial_write(get_capacitor_percent());
		break;
	case BATTERY:
		serial_write(get_battery_percent());
		break;
	case TEST:
		test();
		break;
    default:
      return false;
      break;
  }
  return true;
}



void TIMEOUT_ISR() {
  reset_decoder();
}
