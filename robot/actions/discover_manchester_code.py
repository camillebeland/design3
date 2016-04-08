from robot.action import Action


class DiscoverManchesterCodeAction(Action):
    def start(self):
        print('Discovering Manchester Code')
        self._context.robot.find_manchester_code()
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotImplementedError
