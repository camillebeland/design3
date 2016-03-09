class DoubleSidedBuffer:
    def __init__(self):
        self.writter = None
        self.reader = None

    def write(self, data):
        self.writter = data
        self.__swapbuffers()

    def __swapbuffers(self):
        self.writter, self.reader = self.reader, self.writter

    def read(self):
        return self.reader
