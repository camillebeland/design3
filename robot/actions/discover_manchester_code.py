from robot.action import Action


class DiscoverManchesterCodeAction(Action):
    def start(self):
        self.running = True
        print('Discovering Manchester Code')
        try:
            self._context.robot.find_manchester_code()
        except Exception as e:
            self.running = False
            print(e)
        if self.running:
            self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        print("Discover manchester code asked to stop")
        self.running = False

