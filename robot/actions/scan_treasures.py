from robot.action import Action
from robot.vision.treasure_angle_to_worldmap_positon_converter import TreasureAngleToWorldmapPositionConverter


class ScanTreasuresAction(Action):
    def __rotate(self):
        robot_angle = self._context.worldmap.get_robot_angle()
        self._context.robot.rotate(180 - robot_angle, self.scan_treasures())

    def start(self):
        # TODO
        raise NotImplementedError
        self.__rotate()

    def scan_treasures(self):
        treasures_positon_converter = TreasureAngleToWorldmapPositionConverter(
            self._context.worldmap.table_calibration_service,
            self._context.embedded_camera.get_treasure_angles(), self._context.robot)

        treasures = treasures_positon_converter.get_treasures()
        self._context.worldmap.worldmap_service.add_treasures(treasures)
