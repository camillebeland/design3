from datetime import datetime, timedelta


class Timer:
    def __init__(self):
        self.is_running = False
        self.time_since_start = timedelta()

    def start(self):
        self.is_running = True
        self.start_time = datetime.now()

    def stop(self):
        self.is_running = False

    def __time_since_start(self):
        if self.is_running:
            self.time_since_start = datetime.now() - self.start_time
        return self.time_since_start

    def get_time_since_beginning(self):
        return self.__time_since_start().seconds
