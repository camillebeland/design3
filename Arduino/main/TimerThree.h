#ifndef TimerThree_h
#define TimerThree_h

#define RESOLUTION 65536
#define CPU_FREQUENCY 16000000
#define PRESCALER 256


class TimerThree{

public:
	void init(int freq, void (*isr)());
	void start();
	void stop();
	int counter;
	void (*isrCallback)();
};

extern TimerThree Timer3;

#endif 
