#include "TimerThree.h"
#include <avr/io.h>
#include <avr/interrupt.h>

TimerThree Timer3;

ISR(TIMER3_OVF_vect)          // interrupt service routine that wraps a user defined function supplied by attachInterrupt
{
	TCNT3 = Timer3.counter; // reload
	Timer3.isrCallback(); // ISR
}


void TimerThree::init(int freq, void (*isr)()){
	
	isrCallback = isr;
	Timer3.counter = RESOLUTION-((CPU_FREQUENCY/PRESCALER)/freq);
	TCCR3A = 0;
	TCCR3B = 0;
	TIMSK3 |= (1 << TOIE3);   // enable timer overflow interrupt
	//TIMSK1 &= ~_BV(TOIE1);   // disable timer overflow interrupt
	//TCNT1 = counter;
}

void TimerThree::start(){
	TCNT3 = Timer3.counter; // reload
	TCCR3B |=  (1 << CS32);  //  256 prescaler
}

void TimerThree::stop(){
	TCCR3B  = 0;
}
