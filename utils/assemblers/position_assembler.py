from utils.dto.position import Position


class PositionAssembler:
    def from_dict(self, position_dict):
        x = position_dict['x']
        y = position_dict['y']
        return Position(x, y)
