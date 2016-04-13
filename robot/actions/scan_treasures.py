from robot.action import Action
from robot.treasure_angle_to_worldmap_positon_converter import TreasureAngleToWorldmapPositionConverter


class ScanTreasuresAction(Action):
    def __rotate(self):
        self.running = True
        self._context.robot.rotate_to(180, self.scan_treasures)

    def start(self):
        self.__rotate()

    def scan_treasures(self):
        treasures_position_converter = TreasureAngleToWorldmapPositionConverter(
            self._context.worldmap.table_calibration_service,
            self._context.embedded_camera.get_treasure_angles(), self._context.robot)

        treasures = treasures_position_converter.get_treasures()
        self._context.worldmap.add_treasures(treasures)
        print(self._context.worldmap.worldmap_service, self._context.worldmap.worldmap_service.get_treasures())

        if self.running:
            self._context.event_listener.notify_event(self._end_message)
        self.running = False

    def stop(self):
        print("Scan treasures asked to stop")
        self.running = False

