from robot.action import Action
from time import sleep


class RefreshImageAction(Action):
    def start(self):
        self.running = True
        self._context.vision_refresher.refresh(self.refresh_done)

    def refresh_done(self):
        if self.running:
            self._context.event_listener.notify_event(self._end_message)
            self.running = False

    def stop(self):
        print("Refresh image asked to stop")
        self.running = False

