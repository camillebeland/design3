from robot.action import Action

class DiscoverManchesterCodeAction(Action):
    def start(self):
        print('Discovering Manchester Code')
        try:
             self._context.robot.find_manchester_code()
        except Exception as e:
            print(e)
        self._context.event_listener.notify_event(self._end_message)

    def stop(self):
        raise NotImplementedError
