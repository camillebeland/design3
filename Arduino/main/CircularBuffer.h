#ifndef CircularBuffer_h
#define CircularBuffer_h



class CircularBuffer{

public:
	CircularBuffer(int size);
	CircularBuffer(CircularBuffer &copy);
	void write(int data);
	void read(int * ptr);
	int read();
	~CircularBuffer(); 
private:
	int *buffer;
	int readIndex;
	int writeIndex;
	int bufferSize;
};
#endif 
