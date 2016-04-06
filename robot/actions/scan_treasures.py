from robot.action import Action
from robot.treasure_angle_to_worldmap_positon_converter import TreasureAngleToWorldmapPositionConverter


class ScanTreasuresAction(Action):
    def start(self):
        treasures_positon_converter = TreasureAngleToWorldmapPositionConverter(self._worldmap.table_calibration_service,
                                                                   self._embedded_camera.get_treasure_angles(),
                                                                   self._robot)
        treasures = treasures_positon_converter.get_treasures()
        print(treasures)