from utils.dto.robot_info import RobotInfo


class RobotInfoAssembler:
    def __init__(self, position_assembler):
        self.position_assembler = position_assembler

    def from_dict(self, robot_info_dict):
        position_dict = robot_info_dict['position']
        position = self.position_assembler.from_dict(position_dict)
        angle = robot_info_dict['angle']
        return RobotInfo(position, angle)


