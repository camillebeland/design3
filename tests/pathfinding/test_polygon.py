from pathfinding.polygon import Polygon
from utils.position import Position
from math import sqrt
from nose.tools import *


class TestPolygon:
    def test_distance_should_return_euclidian_distance(self):
        # Given
        polygon = Polygon(x=0, y=0, size=0)
        target = Position(5, 5)
        expected_distance = sqrt(25+25)

        # When
        actual_distance = polygon.distance(target)

        # Then
        assert_equals(expected_distance, actual_distance)

