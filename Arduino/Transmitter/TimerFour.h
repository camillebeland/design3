#ifndef TimerFour_h
#define TimerFour_h

#define RESOLUTION 65536
#define CPU_FREQUENCY 16000000
#define PRESCALER 256


class TimerFour{

public:
	void init(int freq, void (*isr)());
	void start();
	void stop();
	int counter;
	void (*isrCallback)();
};

extern TimerFour Timer4;

#endif 
