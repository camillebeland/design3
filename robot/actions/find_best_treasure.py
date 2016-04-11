from robot.action import Action


class FindBestTreasureAction(Action):
    def start(self):
        self.running = True
        print('Finding Best Treasure')
        robot_position = self._context.robot.get_position()
        target_island_position = self._context.robot.get_target_island_position()
        try:
            treasure_position = self._context.treasure_easiest_path.find_easiest_treasure_from(robot_position, target_island_position)
        except Exception as e:
            self.running = False
            print(e)
        self._context.robot.change_target_treasure_position(treasure_position)
        if self.running:
            self._context.event_listener.notify_event(self._end_message)
            self.running = False

    def stop(self):
        print("Find best treasure asked to stop")
        self.running = False

