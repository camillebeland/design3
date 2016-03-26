class RobotInfoAssembler:

    def json_to_robot_info(self, json):
        robot_info = {}
        robot_info['x'] = json['center'][0]
        robot_info['y'] = json['center'][1]
        # robot_info = json['angle']
        return robot_info
