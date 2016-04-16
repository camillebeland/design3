from robot.action import Action
from time import sleep


class StartTimerAction(Action):
    def start(self):
        self.running = True
        self._context.timer.start()
        if self.running:
            self._context.event_listener.notify_event(self._end_message)
            self.running = False

    def stop(self):
        print("Start timer asked to stop")
        self.running = False

