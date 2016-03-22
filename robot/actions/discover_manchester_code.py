from robot.action import Action


class DiscoverManchesterCodeAction(Action):
    def start(self):
        self._robot.find_manchester_code()
