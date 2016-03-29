#include "TimerFour.h"
#include <avr/io.h>
#include <avr/interrupt.h>

TimerFour Timer4;

ISR(TIMER4_OVF_vect)          // interrupt service routine that wraps a user defined function supplied by attachInterrupt
{
	TCNT4 = Timer4.counter; // reload
	Timer4.isrCallback(); // ISR
}


void TimerFour::init(int freq, void (*isr)()){
	
	isrCallback = isr;
	Timer4.counter = RESOLUTION-((CPU_FREQUENCY/PRESCALER)/freq);
	TCCR4A = 0;
	TCCR4B = 0;
	TIMSK4 |= (1 << TOIE4);   // enable timer overflow interrupt
	//TIMSK1 &= ~_BV(TOIE1);   // disable timer overflow interrupt
	//TCNT1 = counter;
}

void TimerFour::start(){
	TCNT4 = Timer4.counter; // reload
	TCCR3B |=  (1 << CS42);  //  256 prescaler
}

void TimerFour::stop(){
	TCCR4B  = 0;
}
